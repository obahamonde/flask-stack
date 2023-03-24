paths = [
    "/etc/nginx/conf.d/",
    "/etc/nginx/sites-enabled/",
    "/etc/nginx/sites-available/"
]

def render_nginx_conf(port:int,domain:str)->str:
    return f"""server {{
    listen 80;
    server_name {domain}.smartpro.solutions;

    location / {{
        proxy_pass http://localhost:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}
}}"""


if __name__ == "__main__":
    port = int(input("Enter port: "))
    domain = input("Enter domain: ")

    nginx_conf = render_nginx_conf(port,domain)
    
    for path in paths:
        with open(path+domain+".conf","w") as f:
            f.write(nginx_conf)
            
    print("Done!")