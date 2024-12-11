from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import subprocess
import os
import signal
import atexit
import uvicorn

app = FastAPI()

# Start the Node.js server as a subprocess
node_process = None

def start_node_server():
    global node_process
    env = os.environ.copy()
    env['NODE_ENV'] = 'production'
    node_process = subprocess.Popen(
        ['pnpm', 'start', '--server-only'],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        env=env
    )

def cleanup():
    if node_process:
        node_process.send_signal(signal.SIGTERM)
        node_process.wait()

atexit.register(cleanup)

@app.on_event("startup")
async def startup_event():
    start_node_server()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    # Forward all requests to the Node.js server
    return JSONResponse({"error": "Please use the Node.js endpoints directly"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
