# flask-project
***
#### Prepared by *Maksym Oliinyk*
***
### Description
Simple application for reservation auditoriums on a specific time.

The application uses RESTful API for storing data and reading from a database.

The application should allow:
* reservation auditoriums for a specific date and time from 1 to 5 hours;
* users must have the ability to reserve auditoriums, edit, cancel and
  delete them;
* warn users about overlays :
  * two users cannot reserve an auditorium for the same time,
  * reservation times must not overlap.

The RESTful API is built using _Flask_ framework and _MySQL_ database.
***
### API endpoints
* **user**
  * POST ('/user') : create and submit user to the server.
  ```json
  {
    "username": "MO",
    "first_name": "Maksym",
    "last_name": "Oliinyk",
    "email": "maks@gmail.com",
    "password": "212121",
    "phone": "2222222",
    "user_status": true
  }
  ```
  * GET ('/user/\<string:username>') : retrieves all data about user from the server by his username.
  _/user/MO_
  * GET ('/user/\<int:id>') : retrieves all data about user from the server by his id.
  _/user/1_
  * PUT ('/user/\<int:id>') : update all user data already on the server.
  _/user/1_
  ```json
  {
    "username": "MO",
    "first_name": "Maksym",
    "last_name": "Oliinyk",
    "email": "maks@gmail.com",
    "password": "new_password",
    "phone": "1111111",
    "user_status": true
  }
  ```
  * DELETE ('/user/\<string:username>') : deletes all user data from the server.
  _/user/MO_
***
### Information links
Below you can find links with the information that I used writing this project:

* [_Flask documentation_](https://flask.palletsprojects.com/en/2.1.x/)
* [_Database connection_](https://www.sqlalchemy.org/)
* [_Data validation_](https://marshmallow.readthedocs.io/en/stable/)
* [_Flask-HTTP authorization_](https://flask-httpauth.readthedocs.io/en/latest/#basic-authentication-examples)
* [_Application testing_](https://docs.python.org/3/library/unittest.html)
***