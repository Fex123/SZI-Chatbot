"""
Gunicorn configuration file
"""
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:3104"
backlog = 2048

# Worker processes - adjust for your use case
# For a development environment, 2-4 workers is usually sufficient
workers = 4
worker_class = 'sync'
worker_connections = 1000
timeout = 60  # Increased timeout for long-running API calls
keepalive = 2

# Logging
loglevel = 'info'
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
capture_output = True  # Capture print statements from the application
forwarded_allow_ips = '*'  # Allow X-Forwarded-For header from all IPs

# Process naming
proc_name = 'szi-chatbot-api'

# Application preload - Optional, but can improve performance
# by loading the app once before forking
preload_app = False  # Set to True if your app is thread-safe and has no global state issues

# Server hooks
def post_fork(server, worker):
    # This runs for each worker after fork - good place to initialize worker-specific resources
    server.log.info(f"Worker {os.getpid()} initialized")

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info(f"Server is ready. Spawning {workers} workers")
    
def worker_exit(server, worker):
    # Clean up any resources when a worker exits
    server.log.info(f"Worker {os.getpid()} exiting")
