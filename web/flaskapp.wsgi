[server:main]
use = egg:gunicorn#main
host = 127.0.0.1
port = 8080
workers = 3