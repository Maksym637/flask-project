from run_app import app
from models import Session, User
import unittest


class TestUser(unittest.TestCase):
    """_summary_
    Testing all user methods.
    I define two methods : setUp() and tearDown() (setUp - adds all prerequisite steps, tearDown - clean-up all steps).
    After that tests : POST, GET, PUT and DELETE are tested below.
    """

    url = '/user'

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
        
    def test_retrieve(self):
        user = {
            "username": "UT",
            "first_name": ".......",
            "last_name": ".......",
            "email": ".......",
            "password": "21212121",
            "phone": ".......",
            "user_status": True
            }
        created = self.client.post(self.url, json=user)

        url_id = f'/user/{created.json["id"]}'
        response = self.client.get(url_id)
        self.assertEqual(response.status_code, 200)

        url_username = f'/user/{created.json["username"]}'
        response = self.client.get(url_username)
        self.assertEqual(response.status_code, 200)
    
    def test_retrieve_error(self):
        url_id = '/user/100000'
        response = self.client.get(url_id)
        self.assertEqual(response.status_code, 404)

        url_username = '/user/USERNAME'
        response = self.client.get(url_username)
        self.assertEqual(response.status_code, 404)
    
    def test_update(self):
        user = {
            "username": "UT",
            "first_name": ".......",
            "last_name": ".......",
            "email": ".......",
            "password": "21212121",
            "phone": ".......",
            "user_status": True
            }
        created = self.client.post(self.url, json=user)

        url_id = f'/user/{created.json["id"]}'
        updated_fields = {
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "password": "45454545"
        }
        response = self.client.put(url_id, json=updated_fields)
        self.assertEqual(response.status_code, 200)

        expected_first_name, expected_last_name = "updated_first_name", "updated_last_name"
        actual_first_name, actual_last_name = response.json["first_name"], response.json["last_name"]
        self.assertEqual(actual_first_name, expected_first_name)
        self.assertEqual(actual_last_name, expected_last_name)

        updated_errors = [{
            "first_name": True,
            "last_name": "updated_last_name",
            "password": "45454545"
        },
        {
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "password": "111"
        }]
        for i in range(len(updated_errors)):
            response = self.client.put(url_id, json=updated_errors[i])
            self.assertEqual(response.status_code, 400)
    
    def test_update_error(self):
        url_id = '/user/100000'
        updated_fields = {
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "password": "45454545"
        }
        response = self.client.put(url_id, json=updated_fields)
        self.assertEqual(response.status_code, 404)
    
    def test_delete(self):
        user = {
            "username": "UT",
            "first_name": ".......",
            "last_name": ".......",
            "email": ".......",
            "password": "21212121",
            "phone": ".......",
            "user_status": True
            }
        created = self.client.post(self.url, json=user)

        url_username = f'/user/{created.json["username"]}'
        response = self.client.delete(url_username)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_error(self):
        url_username = '/user/USERNAME'
        response = self.client.delete(url_username)
        self.assertEqual(response.status_code, 404)