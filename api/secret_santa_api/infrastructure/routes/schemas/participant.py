from marshmallow import Schema, fields, validate


class AddParticipantRequestSchema(Schema):
    name = fields.Str(required=True, validate=[validate.Length(min=1, max=100)])
    email = fields.Str(
        required=True, validate=validate.Email(error="Not a valid email address")
    )
