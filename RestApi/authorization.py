from models import Session, User
from flask_bcrypt import check_password_hash
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = Session.query(User).filter_by(username=username).first()
    if user is not None and check_password_hash(user.password, password):
        return username