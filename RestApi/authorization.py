from flask_bcrypt import check_password_hash
from flask_httpauth import HTTPBasicAuth
from models import Session, User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    """Checks the correctness of the entered password

    Args:
        username (str): entered username
        password (str): entered password

    Returns:
        str: correct username
    """
    user = Session.query(User).filter_by(username=username).first()
    if user is not None and check_password_hash(user.password, password):
        return username
    return None
