from flask import Flask, request, jsonify
import subprocess
import os
import signal
import atexit

app = Flask(__name__)

# Start the Node.js server as a subprocess
node_process = None

def start_node_server():
    global node_process
    env = os.environ.copy()
    env['NODE_ENV'] = 'production'
    node_process = subprocess.Popen(
        ['pnpm', 'start', '--server-only'],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        env=env
    )

def cleanup():
    if node_process:
        node_process.send_signal(signal.SIGTERM)
        node_process.wait()

atexit.register(cleanup)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Forward all requests to the Node.js server
    return jsonify({'error': 'Please use the Node.js endpoints directly'})

if __name__ == '__main__':
    start_node_server()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
