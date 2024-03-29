from marshmallow import Schema, fields

class UserSchema(Schema):
    """_summary_
    Describes the user schema with all fields
    """
    id = fields.Integer()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String()
    password = fields.String()
    phone = fields.String()
    user_status = fields.Boolean()


class AuditoriumSchema(Schema):
    """_summary_
    Describes the auditorium schema with all fields
    """
    id = fields.Integer()
    number = fields.Integer()
    max_people = fields.Integer()
    is_free = fields.Boolean()


class AccessSchema(Schema):
    """_summary_
    Describes the access schema with all fields
    """
    id = fields.Integer()
    auditorium_id = fields.Integer()
    user_id = fields.Integer()
    start = fields.DateTime()
    end = fields.DateTime()


class LoginSchema(Schema):
    """_summary_
    Describes the login schema with all fields
    """
    username = fields.String()
    password = fields.String()
