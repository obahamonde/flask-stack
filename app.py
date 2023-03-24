"""App entry point."""
from flask import request, Request, Response, jsonify, redirect
from src import FlaskStack
from src.tasks import task, cache
from werkzeug.exceptions import HTTPException

app = FlaskStack(__name__)

@app.get("/")
def index():
    """Index page."""
    return jsonify({"message": "Hello World!"})


@app.get("/api/health")
def healthcheck():
    """Healthcheck endpoint."""
    return jsonify({"message": "Stack is healthy", "status": "success"})
    

@app.get("/dashboards/rabbitmq")
def rabbitmq():
    """Queue Dashboard."""
    return redirect(url="http://localhost:15672")


@app.get("/dashboards/minio")
def minio():
    """Bucket Dashboard."""
    return redirect(url="http://localhost:9001")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4444)