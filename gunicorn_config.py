# Gunicorn configuration file
workers = 4  # Number of worker processes
worker_class = 'sync'
bind = '0.0.0.0:5000'
timeout = 120  # Timeout in seconds
worker_connections = 1000
keepalive = 5
threads = 4
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = 'info'
