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

titles={
    "en":{
        "search":"Search for",
        "desc":"What is it?",
        "symptoms":"What are the symptoms?",
        "treatment":"How do we treat it?",
        "lifestyle":"What lifestyle changes could I make?",
        "meds":"What are the medications used to treat this?",
        "interactions":"Interactions"
    },
    "es":{
        "search":"Buscar por",
        "desc":"¿Qué es?",
        "symptoms":"¿Qué síntomas tienes?",
        "treatment":"¿Cómo la tratamos?",
        "lifestyle":"¿Qué cambios de estilo de vida podría hacer?",
        "meds":"¿Cuáles son los medicamentos utilizados para tratar esto?",
        "interactions":"Interacciones con ortos medicamentos"
    },
    "de":{
        "search":"Suche nach",
        "desc":"Was ist das?",
        "symptoms":"Welche Symptome können auftreten?",
        "treatment":"Wie gehen wir damit um?",
        "lifestyle":"Welche Änderungen des Lebensstils könnte ich vornehmen?",
        "meds":"Welche Medikamente werden verwendet, um dies zu behandeln?",
        "interactions":"Interaktionen"
    },
    "dz":{
        "search":"འཚོལ་ཞིབ་འབད་",
        "desc":"འདི་ག་ཅི་ཨིན་ན་?",
        "symptoms":"ཌེང་གི་གི་གི་ནད་གཞི་འདི་ག་ཅི་ཨིན་ན?",
        "treatment":"ང་བཅས་ཀྱིས་དེ་ ག་དེ་སྦེ་ལག་ལེན་འཐབ་ནི་ཨིན་ན?",
        "lifestyle":"ང་བཅས་རའི་མི་ཚེ་འདི་ ག་ཅི་བཟུམ་ཅིག་ལུ་འགྱུར་ནི་ཡོདཔ་ཨིན་ན?",
        "meds":"འདི་གི་དོན་ལུ་ ལག་ལེན་འཐབ་མི་སྨན་ཚུ་ག་ཅི་ཡོདཔ་ཨིན་ན?",
        "interactions":"འབྲེལ་བ་འཐབ་ཐབས།"
    },
    "ne":{
        "search":"यसका लागि खोजी गर्नुहोस्:",
        "desc":"यो के हो? ",
        "symptoms":"लक्षणहरू के के हुन्?",
        "treatment":"हामी यसलाई कसरी व्यवहार गर्छौं?",
        "lifestyle":"मैले कस्तो जीवनशैली परिवर्तन गर्न सक्छु?",
        "meds":"यसको उपचार गर्न प्रयोग गरिने औषधीहरू के के हुन्?",
        "interactions":"अन्तरक्रिया"
    }
}

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
        resp.set_cookie(key='language',value=lang, secure=False, httponly=False, path='/', max_age=3600, domain=None)
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
    cookie_lang = request.cookies.get('language')
    condition_name = request.args.get('condition')
    condition_name = f"{cookie_lang}_{condition_name}"
    if condition_name not in conditions_json:
        return render_template("not_found.html", condition=condition_name)
    res = conditions_json[condition_name]
    if 'extra' in res:
        return render_template(
            'condition.html',
            condition = res["condition"],
            description = res["description"],
            symptoms = res["symptoms"],
            treatment = res["treatment"],
            lifestyle = res["lifestyle"],
            medications = res["medications"],
            headers=titles[cookie_lang],
            extra=res['extra']
        )
    else:
        return render_template(
            'condition.html',
            condition = res["condition"],
            description = res["description"],
            symptoms = res["symptoms"],
            treatment = res["treatment"],
            lifestyle = res["lifestyle"],
            medications = res["medications"],
            headers=titles[cookie_lang],
            extra=None
        )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    print(f"Condition Collection running on {host}:{port}")
    app.run(host=host, port=port, debug=True)