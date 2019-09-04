import unittest
from unittest.mock import patch

from app import app


class TestViews(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.headers = {'user_name': 'andrew'}

    @patch('views.Project.add_project')
    def test_add_project(self, mock_add_project):
        response = self.client.post('/projects/test', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'result': 'success'})

    @patch('views.Project.get_projects')
    def test_get_projects(self, mock_get_projects):
        mock_get_projects.return_value = [{'project_name': 'test'}]
        response = self.client.get('/projects', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'projects': [{'project_name': 'test'}]})

    @patch('views.Project.delete_project')
    @patch('views.Project.is_owner')
    def test_delete_projects(self, mock_is_owner, mock_delete_project):
        mock_is_owner.return_value = True
        response = self.client.delete('/projects/test', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"response": "project deleted"})

    @patch('views.Project.delete_project')
    @patch('views.Project.is_owner')
    def test_delete_projects_unauthorized(self, mock_is_owner, mock_delete_project):
        mock_is_owner.return_value = False
        response = self.client.delete('/projects/test', headers=self.headers)
        self.assertEqual(response.status_code, 401)

    @patch('views.Transaction.add_transaction')
    @patch('views.Project.is_owner')
    def test_create_transaction(self, mock_is_owner, mock_add_transaction):
        mock_is_owner.return_value = True
        transaction_data = {
            "acquirer_name": "August Equity",
            "target_id": "04220636",
            "target_name": "Wax Digital",
            "value": "15000000"
        }
        response = self.client.post('/projects/test/transactions', headers=self.headers, json=transaction_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"result": "success"})

    @patch('views.Project.is_owner')
    def test_create_transaction_unauthorized(self, mock_is_owner):
        mock_is_owner.return_value = False
        response = self.client.post('/projects/test/transactions', headers=self.headers)
        self.assertEqual(response.status_code, 401)

    @patch('views.Transaction.add_transaction')
    @patch('views.Project.is_owner')
    def test_create_transaction_bad_response(self, mock_is_owner, mock_add_transaction):
        mock_is_owner.return_value = True
        transaction_data = {
            "acquirer_name": "August Equity",
            "target_id": "04220636",
            "target_name": "Wax Digital",
        }
        response = self.client.post('/projects/test/transactions', headers=self.headers, json=transaction_data)
        self.assertEqual(response.status_code, 400)

    @patch('views.Transaction.get_all_transactions_for_project')
    def test_get_all_transactions_for_project(self, mock_get_all_transactions_for_project):
        mock_get_all_transactions_for_project.return_value = [{'transaction': 'test'}]
        response = self.client.get('/projects/<project_name>/transactions', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"transactions": [{'transaction': 'test'}]})

    @patch('views.Transaction.delete_transaction')
    @patch('views.Project.is_owner')
    def test_delete_transaction(self, mock_is_owner, mock_get_all_transactions_for_project):
        mock_is_owner.return_value = True
        response = self.client.delete('/projects/test/transactions/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"result": "success"})

    @patch('views.Transaction.delete_transaction')
    @patch('views.Project.is_owner')
    def test_delete_transaction_unauthorized(self, mock_is_owner, mock_get_all_transactions_for_project):
        mock_is_owner.return_value = False
        response = self.client.delete('/projects/test/transactions/1', headers=self.headers)
        self.assertEqual(response.status_code, 401)
