from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import subprocess
import os
import signal
import atexit
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Eliza Agent")

# Start the Node.js server as a subprocess
node_process = None

def start_node_server():
    global node_process
    try:
        env = os.environ.copy()
        env['NODE_ENV'] = 'production'
        node_process = subprocess.Popen(
            ['pnpm', 'start'],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info("Node.js server started successfully")
    except Exception as e:
        logger.error(f"Failed to start Node.js server: {e}")
        sys.exit(1)

def cleanup():
    if node_process:
        logger.info("Shutting down Node.js server")
        node_process.send_signal(signal.SIGTERM)
        node_process.wait()

atexit.register(cleanup)

@app.on_event("startup")
async def startup_event():
    start_node_server()

@app.get("/health")
async def health():
    if node_process and node_process.poll() is None:
        return {"status": "ok", "node_server": "running"}
    return JSONResponse(
        status_code=500,
        content={"status": "error", "node_server": "not running"}
    )
