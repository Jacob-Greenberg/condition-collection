from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
import translate
import os

# Load environment variables from .env file
load_dotenv()

# Get the host and port from environment variables
host = os.getenv('HOST')
port = os.getenv('PORT')

if host == None:
    host = '127.0.0.1'
if port == None:
    port = '5000'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    print(f"Condition Collection running on {host}:{port}")
    app.run(host=host, port=port, debug=True)