from models import Session
from flask import jsonify, request, Response, Blueprint
from marshmallow import ValidationError
from models import User, Auditorium, Access
from schemas import AccessSchema
from datetime import datetime, timedelta
from authorization import auth
from sqlalchemy import and_


access = Blueprint("access", __name__)


@access.route("/access", methods=["POST"])
@auth.login_required
def create_access():
    """_summary_
    Create and submit reservation to the server.

    Returns:
        json: returns all reservation attributes.
    """

    data = request.get_json(force=True)

    login_entry = Session.query(User).filter_by(username=auth.current_user()).first()
    if login_entry.id != int(data.get('user_id')):
        return Response(status=401, response="[YOU CANNOT BOOK AUDITORIUM FOR ANOTHER PERSON]")

    try:
        AccessSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400

    start = request.json.get('start', None)
    end = request.json.get('end', None)
    start_time = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    time = end_time - start_time

    # Check the correctness of the time
    if start_time < datetime.now() or end_time < datetime.now():
        return Response(status=400, response="[YOU CANNOT BOOK AUDITORIUM IN THE PAST]")
    elif time <= timedelta(hours=1):
        return Response(status=400, response="[INVALID ACCESS TIME (TOO SHORT)]")
    elif time >= timedelta(hours=5):
        return Response(status=400, response="[INVALID ACCESS TIME (TOO LONG)]")

    auditorium_id = int(request.json.get('auditorium_id', None))
    auditoriums = Session.query(Access).all()

    # Check for overlays with the reservation of auditoriums
    for auditorium in auditoriums:
        if auditorium.auditorium_id != auditorium_id:
            continue
        db_start_time = auditorium.start
        db_end_time = auditorium.end
        if start_time <= db_start_time and db_end_time <= end_time:
            return Response(status=403, response="[TIME RESERVED : 1]") # {  []  }
        elif start_time > db_start_time and db_end_time > end_time:
            return Response(status=403, response="[TIME RESERVED : 2]") # [  {}  ]
        elif start_time < db_start_time and end_time > db_start_time:
            return Response(status=403, response="[TIME RESERVED : 3]") # { [ } ]
        elif start_time < db_end_time and end_time > db_end_time:
            return Response(status=403, response="[TIME RESERVED : 4]") # [ { ] }

    try:
        entry = Access(**data)
        Session.add(entry)
        Session.commit()
    except:
        return "[SUCH USER OR AUDITORIUM NOT FOUND]", 404
    
    return jsonify(AccessSchema().dump(entry))


@access.route("/access/<int:user_id>", methods=["GET"])
def get_access(user_id):
    """_summary_
    Retrieves all data about reservation from the server by user_id.

    Args:
        user_id (int): user's primary key

    Returns:
        json: returns all reservation attributes.
    """

    entry = Session.query(User).filter_by(id=user_id).first()
    if entry is None:
        return Response(status=404, response="[SUCH USER ID DOES NOT EXIST. THUS, THERE ARE NO RESERVATION FOR HIM]")
    entries = Session.query(Access).filter_by(user_id=user_id).all()
    return jsonify(AccessSchema(many=True).dump(entries))


@access.route("/access", methods=["GET"])
def get_accesses():
    """_summary_
    Retrieves all data about access from the server.

    Returns:
        json: returns all accesses attributes.
    """

    entries = Session.query(Access).all()
    return jsonify(AccessSchema(many=True).dump(entries))


@access.route("/access/<int:auditorium_id>", methods=["DELETE"])
@auth.login_required
def delete_access(auditorium_id):
    """_summary_
    Deletes all reservation data from the server.

    Args:
        auditorium_id (int): auditorium's primary key

    Returns:
        json: returns all reservation attributes.
    """
    
    entry = Session.query(Auditorium).filter_by(id=auditorium_id).first()
    if entry is None:
        return Response(status=404, response="[SUCH AUDITORIUM ID DOES NOT EXIST]")

    access = Session.query(Access).filter_by(auditorium_id=auditorium_id).first()
    login_entry = Session.query(User).filter_by(username=auth.current_user()).first()
    login_access_user = Session.query(Access).filter(and_(Access.user_id == login_entry.id, Access.auditorium_id == auditorium_id)).first()
    if access is None:
        return Response(status=404, response="[THERE IS NO RESERVATION FOR THIS AUDITORIUM]")
    if not login_access_user:
        return Response(status=401, response="[YOU HAVE NO ACCESS]")
    Session.delete(access)
    Session.commit()

    return jsonify(AccessSchema().dump(access))