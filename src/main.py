"""Modulew that generates the automatic documentation and wraps the method in a function that validates the parameters"""
from typing import Callable
from json import dumps, loads
from inspect import signature
from functools import wraps
from flask import Flask, request, g, session, current_app, Response, jsonify
from redis import Redis
from src.config import Settings
from src.resource import Resource
from datetime import datetime
from socket import gethostname
from uuid import uuid4


db = Redis("redis", 6379, 1, decode_responses=True)
db_ = Redis("redis", 6379, 2, decode_responses=True)


class FlaskStack(Flask):
    """Database wrapper for Flask
       Wrapper for Flask"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.open_api = []
        self.config.from_object(Settings())
                
        @self.get("/api/docs")
        def docs():
            """Returns the documentation of the API"""
            return jsonify(self.open_api)
        
        @self.get("/api/requests")
        def request_metrics():
            """Returns the request metrics for further analysis via a dashboard"""
            return jsonify([loads(db.get(key)) for key in db.keys()])
        
        @self.get("/api/responses")
        def response_metrics():
            """Returns the response metrics for further analysis via a dashboard"""
            return jsonify([loads(db_.get(key)) for key in db_.keys()])
        
        @self.before_request
        def metrics():
            if request.path not in ["/api/docs", "/api/requests", "/api/responses"]:
                g.data = {
                    "X-Request-id":str(uuid4()),
                    "time" : datetime.now().timestamp(),
                    "ip": request.remote_addr,
                    "host": gethostname(),
                    "method": request.method,
                    "url": request.url,
                    "path": request.path,
                    "query": dict(request.args),
                    "headers": dict(request.headers), 
                    "cookies": dict(request.cookies),
                    
                }
                db.set(g.data["time"], dumps(g.data), ex=7*24*60*60)            

        @self.after_request
        def after_request(response:Response):
            if request.path not in ["/api/docs", "/api/requests", "/api/responses"]:
                g.data = {
                    "time" : g.data["time"],
                    "duration": datetime.now().timestamp() - g.data["time"],
                    "status": response.status_code,
                    "headers": dict(response.headers),
                    "data": str(response.data) if response.data else ""
                }
                db_.set(g.data["time"], dumps(g.data), ex=7*24*60*60)
            return response

    def document(self, rule: str, method: str):
        """function that generates the documentation"""

        def decorator(function_: Callable):
            @wraps(function_)
            def wrapper(**kwargs):
                for key, value in request.args.items():
                    if key in signature(function_).parameters.keys():
                        kwargs[key] = value
                return function_(**kwargs)

            name = function_.__name__
            path_params = []
            query_params = []
            body = None
            response_ = None
            for key in function_.__annotations__.keys():
                if key != "return" and key in rule:
                    path_params.append(
                        {
                            "name": key,
                            "type": function_.__annotations__[key].__name__,
                            "required": True,
                        }
                        if key in function_.__annotations__.keys()
                        else {
                            "name": key,
                            "type": function_.__annotations__[key].__name__,
                            "required": False,
                        }
                    )
                elif (
                    key != "return"
                    and key not in rule
                    and function_.__annotations__[key].__base__.__name__ != "BaseModel"
                ):
                    query_params.append(
                        {
                            "name": key,
                            "type": function_.__annotations__[key].__name__,
                            "required": True,
                        }
                        if key in function_.__annotations__.keys()
                        else {
                            "name": key,
                            "type": function_.__annotations__[key].__name__,
                            "required": False,
                        }
                    )
                elif (
                    key != "return"
                    and function_.__annotations__[key].__base__.__name__ == "BaseModel"
                ):
                    body = function_.__annotations__[key].schema()
                elif key == "return":
                    response_ = function_.__annotations__[key].__name__
                else:
                    continue
            self.open_api.append(
                {
                    "name": name,
                    "method": method,
                    "description": function_.__doc__,
                    "url": rule,
                    "query": query_params,
                    "path": path_params,
                    "body": body,
                    "response": response_,
                }
            )
            return wrapper

        return decorator

    def get(self, rule: str, **options):
        """get method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "GET", **options)(function_),
                methods=["GET"],
            )

        return decorator

    def post(self, rule: str, **options):
        """post method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "POST", **options)(function_),
                methods=["POST"],
            )

        return decorator

    def put(self, rule: str, **options):
        """put method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "PUT", **options)(function_),
                methods=["PUT"],
            )

        return decorator

    def delete(self, rule: str, **options):
        """delete method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "DELETE", **options)(function_),
                methods=["DELETE"],
            )

        return decorator

    def patch(self, rule: str, **options):
        """patch method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "PATCH", **options)(function_),
                methods=["PATCH"],
            )

        return decorator

    def head(self, rule: str, **options):
        """head method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "HEAD", **options)(function_),
                methods=["HEAD"],
            )

        return decorator

    def options(self, rule: str, **options):
        """options method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "OPTIONS", **options)(function_),
                methods=["OPTIONS"],
            )

        return decorator

    def trace(self, rule: str, **options):
        """trace method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "TRACE", **options)(function_),
                methods=["TRACE"],
            )

        return decorator

    def connect(self, rule: str, **options):
        """connect method decorator"""

        def decorator(function_: Callable):
            self.add_url_rule(
                rule,
                view_func=self.document(rule, "CONNECT", **options)(function_),
                methods=["CONNECT"],
            )

        return decorator

    def use(self, resource: Resource):
        """Adds a resource to the application"""
        self.register_blueprint(resource)
        self.open_api.extend(resource.open_api)
        return self