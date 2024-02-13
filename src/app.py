import os
import signal

from flask import Flask, jsonify, request
from waitress import serve

from utils.script_loader import ScriptLoader

port = 55001

app = Flask(__name__)

script_manager = ScriptLoader()


@app.route("/")
def health():
    return '', 200


@app.route("/script", methods=['POST'])
def load_script():
    res, message = script_manager.load_script(module_name=request.json['module'], path=request.json['path'])

    if not res:
        return jsonify({'result': res, 'message': message}), 400

    return jsonify({'result': res, 'message': ''}), 200


@app.route("/script/unload", methods=['GET'])
def unload_script():
    script_manager.unloadScript()
    return '', 200

# lmao it kills the app dumbass
# leaving this here, so you don't try that again
# @app.route("/quit", methods=['GET'])
# def quit_script():
#     os.kill(os.getpid(), signal.SIGTERM)
#     return None


@app.route('/script/home', methods=['GET'])
def get_home_page():
    if not script_manager.is_loaded():
        return jsonify({'error': 'Script manager not loaded'}), 404
    return jsonify(script_manager.get_home_page()), 200


serve(app, host="0.0.0.0", port=port)
