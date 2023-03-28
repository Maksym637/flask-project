from models import Session, Auditorium
from flask import jsonify, request, Response, Blueprint
from marshmallow import ValidationError
from schemas import AuditoriumSchema

auditorium = Blueprint("auditorium", __name__)


@auditorium.route("/auditorium", methods=["POST"])
def create_auditorium():
    """_summary_
    Create and submit auditorium to the server.

    Returns:
        json: returns all auditorium attributes.
    """

    data = request.get_json(force=True)

    try:
        AuditoriumSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400

    try:
        entry = Auditorium(**data)
        Session.add(entry)
        Session.commit()
    except Exception:
        return "[THIS IS A TYPE ERROR]\n[PLEASE, WRITE CORRECT DATA TYPE]", 400

    return jsonify(AuditoriumSchema().dump(entry))


@auditorium.route("/auditorium", methods=["GET"])
def get_auditoriums():
    """_summary_
    Retrieves all data about auditoriums from the server.

    Returns:
        json: returns all auditoriums attributes.
    """

    entries = Session.query(Auditorium).all()
    return jsonify(AuditoriumSchema(many=True).dump(entries))


@auditorium.route("/auditorium/<int:id>", methods=["GET"])
def get_auditorium_by_id(id):
    """_summary_
    Retrieves all data about auditorium from the server by its id.

    Args:
        id (int): auditorium's primary key

    Returns:
        json: returns all auditorium attributes.
    """

    entry = Session.query(Auditorium).filter_by(id=id).first()
    if entry is None:
        return Response(status=404, response="[SUCH AUDITORIUM ID DOES NOT EXIST]")
    return jsonify(AuditoriumSchema().dump(entry))


@auditorium.route("/auditorium/<int:id>", methods=["PUT"])
def update_auditorium_by_id(id):
    """_summary_
    Update all auditorium data already on the server.

    Args:
        id (int): auditorium's primary key

    Returns:
        json: returns all auditorium attributes.
    """

    entry = Session.query(Auditorium).filter_by(id=id).first()
    if entry is None:
        return Response(
            status=404, response="[SUCH AUDITORIUM DOES NOT EXIST]\n[YOU CAN'T UPDATE IT]"
        )

    data = request.get_json(force=True)
    try:
        AuditoriumSchema().load(data)
    except ValidationError:
        return "[THIS IS A VALIDATION ERROR]", 400

    for key, value in data.items():
        setattr(entry, key, value)

    try:
        Session.add(entry)
        Session.commit()
    except Exception:
        return "[THIS IS A TYPE ERROR]\n[PLEASE, WRITE CORRECT DATA TYPE]", 400

    return jsonify(AuditoriumSchema().dump(entry))


@auditorium.route("/auditorium/<int:id>", methods=["DELETE"])
def delete_auditorium_by_id(id):
    """_summary_
    Deletes all auditorium data from the server.

    Args:
        id (int): auditorium's primary key

    Returns:
        json: returns all auditorium attributes.
    """

    entry = Session.query(Auditorium).filter_by(id=id).first()
    if entry is None:
        return Response(status=404, response="[SUCH AUDITORIUM DOES NOT EXIST]")
    Session.delete(entry)
    Session.commit()
    return jsonify(AuditoriumSchema().dump(entry))
