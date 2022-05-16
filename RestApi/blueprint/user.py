from flask_bcrypt import check_password_hash
from models import Session
from flask import jsonify, request, Response, Blueprint
from marshmallow import ValidationError
from models import User
from schemas import UserSchema, LoginSchema
from authorization import auth
import sqlalchemy
import bcrypt
import base64


user = Blueprint("user", __name__)


def is_short_password(string: str) -> bool:
    """_summary_
    Checks if the password is short.

    Args:
        string (str): password

    Returns:
        bool: if short it returns true, otherwise false.
    """

    return len(string) < 6


def is_simple_password(string: str) -> bool:
    """_summary_
    Checks if the password is simple (eg.: consists with the same symbols).

    Args:
        string (str): password

    Returns:
        bool: if simple it returns true, otherwise false.
    """

    flag = True
    for i in range(len(string)):
        for j in range(len(string) - i):
            if string[i] != string[j]:
                flag = False
    return flag


@user.route("/login", methods=["GET"])
def login_user():
    """_summary_
    An encoded string is created for logging

    Returns:
        str: base64_message
    """
    
    data = request.get_json(force=True)

    try:
        LoginSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400
    
    message = data["username"] + ":" + data["password"]
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    user = Session.query(User).filter_by(username=data["username"]).first()

    if user is not None and check_password_hash(user.password, data["password"]):
        return base64_message
    else:
        return Response(status=404, response="[INVALID PASSWORD OR USERNAME]]")


@user.route("/user", methods=["POST"])
def create_user():
    """_summary_
    Create and submit user to the server.

    Returns:
        json: returns all user attributes.
    """
    
    data = request.get_json(force=True)

    if is_short_password(request.json.get('password', None)):
        return "[THIS PASSWORD IS TOO SHORT]", 400
    elif is_simple_password(request.json.get('password', None)):
        return "[THIS PASSWORD IS VERY SIMPLE]", 400

    try:
        UserSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400
    
    password = request.json.get('password', None)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    data.update({"password": hashed_password})

    try:
        entry = User(**data)
        Session.add(entry)
        Session.commit()
    except Exception as error:
        if isinstance(error, sqlalchemy.exc.IntegrityError):
            return "[DUPLICATE UNIQUE VALUE]", 400
        else:
            return "[THIS IS A TYPE ERROR]\n[PLEASE, WRITE CORRECT DATA TYPE]", 400
    
    return jsonify(UserSchema().dump(entry))


@user.route("/user/<string:username>", methods=["GET"])
@auth.login_required
def get_user_by_username(username):
    """_summary_
    Retrieves all data about user from the server by his username.

    Args:
        username (str): his personal information

    Returns:
        json: returns all user attributes.
    """

    entry = Session.query(User).filter_by(username=username).first()
    login_entry = Session.query(User).filter_by(username=auth.current_user()).first()
    if entry is None:
        return Response(status=404, response="[SUCH USERNAME DOES NOT EXIST]")
    if login_entry.username == username or login_entry.user_status == 1:
        return jsonify(UserSchema().dump(entry))
    return Response(status=401, response="[YOU HAVE NO ACCESS]")


@user.route("/user/<int:id>", methods=["GET"])
@auth.login_required
def get_user_by_id(id):
    """_summary_
    Retrieves all data about user from the server by his id.

    Args:
        id (int): user's primary key

    Returns:
        json: returns all user attributes.
    """

    entry = Session.query(User).filter_by(id=id).first()
    login_entry = Session.query(User).filter_by(username=auth.current_user()).first()
    if entry is None:
        return Response(status=404, response="[SUCH USER ID DOES NOT EXIST]")
    if login_entry.id == id:
        return jsonify(UserSchema().dump(entry))
    return Response(status=401, response="[YOU HAVE NO ACCESS]")


@user.route("/user", methods=["PUT"])
@auth.login_required
def update_user_by_id():
    """_summary_
    Update all user data already on the server.

    Args:
        id (int): user's primary key

    Returns:
        json: returns all user attributes.
    """

    data = request.get_json(force=True)

    if is_short_password(request.json.get('password', None)):
        return "[THIS PASSWORD IS TOO SHORT]", 400
    elif is_simple_password(request.json.get('password', None)):
        return "[THIS PASSWORD IS VERY SIMPLE]", 400
    
    try:
        UserSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400
    password = request.json.get('password', None)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    data.update({"password": hashed_password})

    entry = Session.query(User).filter_by(username=auth.current_user()).first()

    for key, value in data.items():
        setattr(entry, key, value)
    
    try:
        Session.add(entry)
        Session.commit()
    except Exception:
        return "[THIS IS A TYPE ERROR]\n[PLEASE, WRITE CORRECT DATA TYPE]", 400
    
    return jsonify(UserSchema().dump(entry))


@user.route("/user/<string:username>", methods=["DELETE"])
@auth.login_required
def delete_user_by_username(username):
    """_summary_
    Deletes all user data from the server.

    Args:
        username (string): his personal information

    Returns:
        json: returns all user attributes.
    """

    entry = Session.query(User).filter_by(username=username).first()
    login_entry = Session.query(User).filter_by(username=auth.current_user()).first()
    if entry is None:
        return Response(status=404, response="[SUCH USERNAME DOES NOT EXIST]")
    if login_entry.username == username or login_entry.user_status == 1:
        Session.delete(entry)
        Session.commit()
        return jsonify(UserSchema().dump(entry))
    return Response(status=401, response="[YOU HAVE NO ACCESS]")