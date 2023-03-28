import unittest
from run_app import app
from models import Session, Auditorium


class TestAuditorium(unittest.TestCase):
    """_summary_
    Testing all auditorium methods.
    I define two methods : setUp() and tearDown().
    After that tests : POST, GET, PUT and DELETE are tested below.
    """

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def tearDown(self):
        number = 18
        entry = Session.query(Auditorium).filter_by(number=number).first()
        if entry is not None:
            Session.delete(entry)
            Session.commit()
        self.app = None
        self.app_context.pop()
        self.client = None

    url = '/auditorium'

    auditorium = {
        "number": "18",
        "max_people": "400",
        "is_free": True
        }

    def test_create(self):
        response = self.client.post(self.url, json=self.auditorium)
        self.assertEqual(response.status_code, 200)

        expected_max_people = 400
        actual_max_people = response.json["max_people"]
        self.assertEqual(actual_max_people, expected_max_people)

    def test_create_error(self):
        auditoriums = [{
            "number": ".....",
            "max_people": "400",
            "is_free": True
        },
        {
            "number": "30",
            "max_people": "500",
            "is_free": "....."
        }]
        for i in range(len(auditoriums)):
            response = self.client.post(self.url, json=auditoriums[i])
            self.assertEqual(response.status_code, 400)

    def test_retrieve(self):
        created = self.client.post(self.url, json=self.auditorium)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        url_id = f'/auditorium/{created.json["id"]}'
        response = self.client.get(url_id)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_error(self):
        url_id = '/auditorium/100000'
        response = self.client.get(url_id)
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        created = self.client.post(self.url, json=self.auditorium)

        url_id = f'/auditorium/{created.json["id"]}'
        updated_fields = {
            "max_people": "228"
        }
        response = self.client.put(url_id, json=updated_fields)
        self.assertEqual(response.status_code, 200)

        expected_max_people = 228
        actual_max_people = response.json["max_people"]
        self.assertEqual(actual_max_people, expected_max_people)

        updated_errors = [{
            "max_people": "....."
        },
        {
            "is_free": "....."
        }]
        for i in range(len(updated_errors)):
            response = self.client.put(url_id, json=updated_errors[i])
            self.assertEqual(response.status_code, 400)

    def test_update_error(self):
        url_id = '/auditorium/100000'
        updated_fields = {
            "max_people": "228"
        }
        response = self.client.put(url_id, json=updated_fields)
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        created = self.client.post(self.url, json=self.auditorium)

        url_id = f'/auditorium/{created.json["id"]}'
        response = self.client.delete(url_id)
        self.assertEqual(response.status_code, 200)

    def test_delete_error(self):
        url_id = '/auditorium/100000'
        response = self.client.delete(url_id)
        self.assertEqual(response.status_code, 404)
