from flask import Flask, render_template, request, send_from_directory, make_response, redirect
from dotenv import load_dotenv
import json
import translate
import os

# Load environment variables from .env file
load_dotenv()

# Get the host and port from environment variables
host = os.getenv('HOST')
port = os.getenv('PORT')
condition_path = os.getenv('CONDITION_PATH')

if host == None:
    host = '127.0.0.1'
if port == None:
    port = '5000'

condition_files = os.listdir(condition_path)
conditions_json = {}

for file in condition_files:
    with open(os.path.join(condition_path, file)) as file_json:
        conditions_json[file.removesuffix('.json')] = json.load(file_json)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    lang = request.args.get('language')
    try:
        cookie_lang = request.cookies.get('language')
    except TypeError:
        cookie_lang = None

    if cookie_lang is not None:
        print("main")
        return redirect('/main')
    elif lang is not None and cookie_lang is None:
        resp = make_response(redirect('/main'))
        resp.set_cookie(key='language',value=lang, path='/select-language')
        return resp
    else:
        return redirect('/select-language')

@app.route('/select-language', methods=['GET', 'POST'])
def select_language():
    return render_template('select-language.html')

@app.route('/main', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')

@app.route('/condition', methods=['GET', 'POST'])
def condition():
    condition_name = request.args.get('condition')
    res = conditions_json[condition_name]
    return render_template(
        'condition.html',
        condition = res["condition"],
        description = res["description"],
        symptoms = res["symptoms"],
        treatment = res["treatment"],
        lifestyle = res["lifestyle"],
        medications = res["medications"],
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    print(f"Condition Collection running on {host}:{port}")
    app.run(host=host, port=port, debug=True)