from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import subprocess
import os
import signal
import atexit
import logging
import sys
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Eliza Agent")

# Global variables for core systems
node_process = None
agent_runtime = None
memory_manager = None
database_adapter = None

def load_character_config():
    try:
        character_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                    'characters', 'eternalai.character.json')
        with open(character_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load character config: {e}")
        return None

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
    character_config = load_character_config()
    if not character_config:
        logger.error("Failed to load character configuration")
        sys.exit(1)

    start_node_server()
    logger.info("Core systems initialized successfully")

@app.get("/health")
async def health():
    if node_process and node_process.poll() is None:
        return {
            "status": "ok",
            "node_server": "running",
            "core_systems": {
                "agent_runtime": "initialized" if agent_runtime else "not initialized",
                "memory_manager": "initialized" if memory_manager else "not initialized",
                "database_adapter": "initialized" if database_adapter else "not initialized"
            }
        }
    return JSONResponse(
        status_code=500,
        content={"status": "error", "node_server": "not running"}
    )
