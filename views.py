from flask import jsonify, request
from werkzeug.exceptions import BadRequest, Unauthorized

from app import app
from models import Project, Transaction


@app.route('/projects/<project_name>', methods=['POST'])
def add_project(project_name):
    Project.add_project(project_name, request.headers['user_name'])
    return jsonify({'result': 'success'})


@app.route('/projects', methods=['GET'])
def get_projects():
    return jsonify({"projects": Project.get_projects(request.headers['user_name'])})


@app.route('/projects/<project_name>', methods=['DELETE'])
def delete_project(project_name):
    _validate_delete_project(project_name, request.headers.get('user_name'))
    Project.delete_project(project_name)
    return jsonify({"response": "project deleted"})


def _validate_delete_project(project_name, user_name):
    if not Project.is_owner(project_name, user_name):
        raise Unauthorized('You must be the project owner to delete the project')


@app.route('/projects/<project_name>/transactions', methods=['POST'])
def create_transaction(project_name):
    transaction_data = request.json
    _validate_create_transaction(project_name, request.headers.get('user_name'), transaction_data)
    Transaction.add_transaction(
        transaction_data['acquirer_name'],
        transaction_data['target_id'],
        transaction_data['target_name'],
        transaction_data['value'],
        project_name
    )
    return jsonify({"result": "success"})


def _validate_create_transaction(project_name, user_name, transaction_data):
    if not Project.is_owner(project_name, user_name):
        raise Unauthorized('You must be the project owner to delete transactions')
    for value in {'acquirer_name', 'target_id', 'target_name', 'value'}:
        if value not in transaction_data:
            raise BadRequest(f'{value} is required in transaction data')


@app.route('/projects/<project_name>/transactions', methods=['GET'])
def get_all_transactions_for_project(project_name):
    return jsonify({"transactions": Transaction.get_all_transactions_for_project(project_name)})


@app.route('/projects/<project_name>/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(project_name, transaction_id):
    _validate_delete_transaction(project_name, request.headers.get('user_name'))
    Transaction.delete_transaction(transaction_id)
    return jsonify({"result": "success"})


def _validate_delete_transaction(project_name, user_name):
    if not Project.is_owner(project_name, user_name):
        raise Unauthorized('You must be the project owner to delete transactions')
