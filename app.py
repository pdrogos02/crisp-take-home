import json
from flask import Flask, jsonify, request

from crisp_transformation import execute_transformation

app = Flask(__name__)

app.config.from_file("transformation_config.json", load=json.load)

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/crisp_transformation/', methods=['POST'])
def execute_transformation():
    execute_transformation()

    return '', 201, { 'location': f'/crisp_transformation/{employee["id"]}' }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)