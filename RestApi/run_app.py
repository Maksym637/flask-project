from blueprint.user import user
from blueprint.auditorium import auditorium
from blueprint.access import access
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(auditorium)
app.register_blueprint(access)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)