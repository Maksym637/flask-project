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
***
### Information links
Below you can find links with the information that I used writing this project:

[_Flask documentation_](https://flask.palletsprojects.com/en/2.1.x/)

[_Database connection_](https://www.sqlalchemy.org/)

[_Data validation_](https://marshmallow.readthedocs.io/en/stable/)

[_Flask-HTTP authorization_](https://flask-httpauth.readthedocs.io/en/latest/#basic-authentication-examples)

[_Application testing_](https://docs.python.org/3/library/unittest.html)
***