from blueprint.user import user
from blueprint.auditorium import auditorium
from flask import Flask

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(auditorium)

if __name__ == "__main__":
    app.run(debug=True)