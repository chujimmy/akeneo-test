from flask import Blueprint, jsonify, request

from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.errrors import ParticipantAlreadyRegisteredError
from secret_santa_api.infrastructure.routes.exceptions.participant import (
    ApiAddParticipantPayloadBadRequest,
)
from secret_santa_api.infrastructure.routes.schemas.participant import (
    AddParticipantRequestSchema,
)
from secret_santa_api.registry import add_participant, get_all_participants


participant_bp = Blueprint("participant", __name__, url_prefix="/participants")


@participant_bp.route("/", methods=["GET"])
def get_participants_handler():
    participants = get_all_participants.perform()

    return jsonify(
        {
            "participants": [
                {
                    "id": participant.id,
                    "name": participant.name,
                    "email": participant.email,
                }
                for participant in participants
            ]
        }
    )


@participant_bp.route("/", methods=["POST"])
def add_participant_handler():
    try:
        schema = AddParticipantRequestSchema()
        new_participant = schema.load(request.get_json())
    except Exception as e:
        raise ApiAddParticipantPayloadBadRequest(e.messages)

    try:
        participant = add_participant.perform(
            Participant(name=new_participant["name"], email=new_participant["email"])
        )
    except ParticipantAlreadyRegisteredError:
        return jsonify({"error": "Participant already registered (email used)"}), 409

    return (
        jsonify(
            {
                "id": participant.id,
                "name": participant.name,
                "email": participant.email,
            }
        ),
        201,
    )
