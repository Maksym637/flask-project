from run_app import app
from models import Session, User, Auditorium, Access
import unittest


class TestAccess(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
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
        "first_name": "User",
        "last_name": "Test",
        "email": "UT@gmail.com",
        "password": "232323",
        "phone": "2381843",
        "user_status": True
        }
    auditorium = {
        "number": "18",
        "max_people": "400",
        "is_free": True
        }
    
    def test_create_delete(self):
        created_user = self.client.post(self.url_user, json=self.user)
        created_auditorium = self.client.post(self.url_auditorium, json=self.auditorium)

        url_access = '/access'
        access = {
            "auditorium_id": int(created_auditorium.json["id"]),
            "user_id": int(created_user.json["id"]),
            "start":"2022-5-28 11:00:00",
            "end": "2022-5-28 12:30:00"
        }
        response = self.client.post(url_access, json=access)
        self.assertEqual(response.status_code, 200)

        url_acess_delete = f'/access/{created_auditorium.json["id"]}'
        response = self.client.delete(url_acess_delete)
        self.assertEqual(response.status_code, 200)