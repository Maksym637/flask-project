from run_app import app
from models import Session, User
import unittest
import json


class TestUser(unittest.TestCase):
    """_summary_
    Testing all user methods.
    I define two methods : setUp() and tearDown() (setUp - adds all prerequisite steps, tearDown - clean-up all steps).
    After that tests : POST, GET, PUT and DELETE are tested below.
    """

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def tearDown(self):
        username = "UT"
        entry = Session.query(User).filter_by(username=username).first()
        if entry is not None:   
            Session.delete(entry)
            Session.commit()
        self.app = None
        self.app_context.pop()
        self.client = None
    
    url = '/user'

    user = {
            "username": "UT",
            "first_name": ".......",
            "last_name": ".......",
            "email": ".......",
            "password": "21212121",
            "phone": ".......",
            "user_status": True
        }
    
    headers = {"Authorization": f"Basic VVQ6MjEyMTIxMjE="}

    def test_create(self):
        user = {
            "username": "UT",
            "first_name": "User",
            "last_name": "Test",
            "email": "UT@gmail.com",
            "password": "232323",
            "phone": "2381843",
            "user_status": True
            }
        response = self.client.post(self.url, json=user)
        self.assertEqual(response.status_code, 200)

        expected_username, expected_first_name, expected_last_name = "UT", "User", "Test"
        actual_username, actual_first_name, actual_last_name = response.json["username"], response.json["first_name"], response.json["last_name"]
        self.assertEqual(actual_username, expected_username)
        self.assertEqual(actual_first_name, expected_first_name)
        self.assertEqual(actual_last_name, expected_last_name)
    
    def test_create_error(self):
        users = [{
            "username": "UT",
            "first_name": "User",
            "last_name": "Test",
            "email": "UT@gmail.com",
            "password": "111",
            "phone": "2381843",
            "user_status": True
            },
            {
            "username": "UT",
            "first_name": True,
            "last_name": "Test",
            "email": "UT@gmail.com",
            "password": "232323",
            "phone": "2381843",
            "user_status": True
            }]
        for i in range(len(users)):
            response = self.client.post(self.url, json=users[i])
            self.assertEqual(response.status_code, 400)
    
    def test_login(self):
        user = {
            "username": "UT",
            "first_name": "User",
            "last_name": "Test",
            "email": "UT@gmail.com",
            "password": "232323",
            "phone": "2381843",
            "user_status": True
            }
        self.client.post(self.url, json=user)

        url_login = '/login'
        response = self.client.get(url_login, data=json.dumps({"username": "UT", "password": "232323"}))
        self.assertEqual(response.status_code, 200)
    
    def test_retrieve(self):
        created = self.client.post(self.url, json=self.user)

        url_id = f'/user/{created.json["id"]}'
        response = self.client.get(url_id, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        url_username = f'/user/{created.json["username"]}'
        response = self.client.get(url_username, headers=self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_retrieve_error(self):
        self.client.post(self.url, json=self.user)

        url_id = '/user/100000'
        response = self.client.get(url_id, headers=self.headers)
        self.assertEqual(response.status_code, 404)

        url_username = '/user/USERNAME'
        response = self.client.get(url_username, headers=self.headers)
        self.assertEqual(response.status_code, 404)
    
    def test_update(self):
        self.client.post(self.url, json=self.user)

        updated_fields = {
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "password": "45454545"
        }
        response = self.client.put(self.url, json=updated_fields, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        expected_first_name, expected_last_name = "updated_first_name", "updated_last_name"
        actual_first_name, actual_last_name = response.json["first_name"], response.json["last_name"]
        self.assertEqual(actual_first_name, expected_first_name)
        self.assertEqual(actual_last_name, expected_last_name)
    
    def test_update_error(self):
        self.client.post(self.url, json=self.user)

        updated_error = {
            "first_name": True,
            "last_name": "updated_last_name",
            "password": "45454545"
        }
        response = self.client.put(self.url, json=updated_error, headers=self.headers)
        self.assertEqual(response.status_code, 400)
    
    def test_delete(self):
        created = self.client.post(self.url, json=self.user)

        url_username = f'/user/{created.json["username"]}'
        response = self.client.delete(url_username, headers=self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_error(self):
        self.client.post(self.url, json=self.user)

        url_username = '/user/USERNAME'
        response = self.client.delete(url_username, headers=self.headers)
        self.assertEqual(response.status_code, 404)