from run_app import app
from models import Session, User, Auditorium
from datetime import datetime
import unittest


class TestAccess(unittest.TestCase):
    """_summary_
    Testing all access methods.
    I define two methods : setUp() and tearDown() (setUp - adds all prerequisite steps, tearDown - clean-up all steps).
    After that tests : POST, GET, PUT and DELETE are tested below.
    """

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
    
    def tearDown(self):
        username = "UT"
        user = Session.query(User).filter_by(username=username).first()
        number = 18
        auditorium = Session.query(Auditorium).filter_by(number=number).first()
        if user is not None or auditorium is not None:   
            Session.delete(user)
            Session.delete(auditorium)
            Session.commit()
        self.app = None
        self.app_context.pop()
        self.client = None
    
    url_user = '/user'
    url_auditorium = '/auditorium'

    user = {
        "username": "UT",
        "first_name": ".......",
        "last_name": ".......",
        "email": ".......",
        "password": "21212121",
        "phone": ".......",
        "user_status": True
        }
    auditorium = {
        "number": "18",
        "max_people": "400",
        "is_free": True
        }
    
    headers = {"Authorization": f"Basic VVQ6MjEyMTIxMjE="}

    def test_create_delete(self):
        created_user = self.client.post(self.url_user, json=self.user)
        created_auditorium = self.client.post(self.url_auditorium, json=self.auditorium)

        url_access = '/access'
        access = {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 11:00:00",
            "end": "2023-5-28 12:30:00"
        }
        response = self.client.post(url_access, json=access, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        expected_start = "2023-05-28T11:00:00"
        actual_start = response.json["start"]
        self.assertEqual(actual_start, expected_start)

        url_access_delete = f'/access/{created_auditorium.json["id"]}'
        response = self.client.delete(url_access_delete, headers=self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_create_error_time(self):
        created_user = self.client.post(self.url_user, json=self.user)
        created_auditorium = self.client.post(self.url_auditorium, json=self.auditorium)

        url_access = '/access'
        accesses = [{
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2018-5-28 11:00:00",
            "end": "2018-5-28 12:30:00"
        },
        {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 11:00:00",
            "end": "2023-5-28 11:30:00"
        },
        {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 11:00:00",
            "end": "2023-5-28 19:00:00"
        }]
        for i in range(len(accesses)):
            response = self.client.post(url_access, json=accesses[i], headers=self.headers)
            self.assertEqual(response.status_code, 400)
    
    def test_create_error_reservation(self):
        created_user = self.client.post(self.url_user, json=self.user)
        created_auditorium = self.client.post(self.url_auditorium, json=self.auditorium)

        url_access = '/access'
        access = {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 11:00:00",
            "end": "2023-5-28 12:30:00"
        }
        self.client.post(url_access, json=access, headers=self.headers)

        accesses = [{
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 10:00:00",
            "end": "2023-5-28 13:30:00"
        },
        {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 11:10:00",
            "end": "2023-5-28 12:20:00"
        },
        {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 9:00:00",
            "end": "2023-5-28 11:30:00"
        },
        {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 11:30:00",
            "end": "2023-5-28 14:00:00"
        }]
        for i in range(len(accesses)):
            response = self.client.post(url_access, json=accesses[i], headers=self.headers)
            self.assertEqual(response.status_code, 403)
        
        url_access_delete = f'/access/{created_auditorium.json["id"]}'
        response = self.client.delete(url_access_delete, headers=self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_retrieve(self):
        created_user = self.client.post(self.url_user, json=self.user)
        created_auditorium = self.client.post(self.url_auditorium, json=self.auditorium)

        url_access = '/access'
        access = {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 11:00:00",
            "end": "2023-5-28 12:30:00"
        }
        self.client.post(url_access, json=access, headers=self.headers)

        url_access_get = f'/access/{created_user.json["id"]}'
        response = self.client.get(url_access_get)
        self.assertEqual(response.status_code, 200)

        url_access_delete = f'/access/{created_auditorium.json["id"]}'
        response = self.client.delete(url_access_delete, headers=self.headers)
        self.assertEqual(response.status_code, 200)
    
    def test_retrieve_error(self):
        url_access_get = '/access/100000'
        response = self.client.get(url_access_get)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_error(self):
        created_user = self.client.post(self.url_user, json=self.user)
        created_auditorium = self.client.post(self.url_auditorium, json=self.auditorium)

        url_access = '/access'
        access = {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2023-5-28 11:00:00",
            "end": "2023-5-28 12:30:00"
        }
        self.client.post(url_access, json=access, headers=self.headers)

        url_access_delete = '/access/100000'
        response = self.client.delete(url_access_delete, headers=self.headers)
        self.assertEqual(response.status_code, 404)

        self.client.delete(url_access_delete, headers=self.headers)