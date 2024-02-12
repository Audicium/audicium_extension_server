import threading

import flask
from flask import Flask, jsonify, request
from waitress import serve
from multiprocessing import Process
from utils.script_loader import ScriptLoader
from werkzeug.serving import make_server

port = 55001

app = Flask(__name__)

script_manager = ScriptLoader()


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


def start_server():
    global server
    app = flask.Flask('myapp')

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

    @app.route("/quit", methods=['GET'])
    def quit_script():
        stop_server()

    @app.route('/script/home', methods=['GET'])
    def get_home_page():
        if not script_manager.is_loaded():
            return jsonify({'error': 'Script manager not loaded'}), 404
        return jsonify(script_manager.get_home_page()), 200

    server = ServerThread(app)
    server.start()


def stop_server():
    global server
    server.shutdown()


start_server()
