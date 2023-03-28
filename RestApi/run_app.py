from flask import Flask
from flask_cors import CORS
from blueprint.user import user
from blueprint.auditorium import auditorium
from blueprint.access import access

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(auditorium)
app.register_blueprint(access)

CORS(app)

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
