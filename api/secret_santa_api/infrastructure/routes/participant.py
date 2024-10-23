import datetime

from flask import Blueprint, jsonify, request

from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.errrors import (
    BlacklistAlreadyExistError,
    BlacklistNotFoundError,
    ParticipantAlreadyRegisteredError,
    UnknownParticipantError,
)
from secret_santa_api.infrastructure.routes.exceptions.participant import (
    ApiAddParticipantPayloadBadRequest,
)
from secret_santa_api.infrastructure.routes.schemas.participant import (
    AddParticipantRequestSchema,
)
from secret_santa_api.registry import (
    add_participant,
    blacklist_participant,
    delete_blacklist_entry,
    get_all_participants,
)


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
                    "created": participant.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "blacklist": list(participant.blacklist),
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
            Participant(
                name=new_participant["name"],
                email=new_participant["email"],
                created=datetime.datetime.now(datetime.timezone.utc),
            )
        )
    except ParticipantAlreadyRegisteredError:
        return jsonify({"error": "Participant already registered (email used)"}), 409

    return (
        jsonify(
            {
                "id": participant.id,
                "name": participant.name,
                "email": participant.email,
                "created": participant.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "blacklist": [],
            }
        ),
        201,
    )


@participant_bp.route("/<int:gifter_id>/blacklist/<int:receiver_id>", methods=["POST"])
def blacklist_participant_handler(gifter_id: int, receiver_id: int):
    try:
        blacklist = blacklist_participant.perform(gifter_id, receiver_id)

        return (
            jsonify(
                {
                    "id": blacklist.id,
                    "created": blacklist.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "gifter_id": blacklist.gifter.id,
                    "receiver_id": blacklist.receiver.id,
                }
            ),
            201,
        )

    except UnknownParticipantError:
        return jsonify({"error": "Unknown participant"}), 400
    except BlacklistAlreadyExistError:
        return jsonify({"error": "Blacklist already exist"}), 409


@participant_bp.route(
    "/<int:gifter_id>/blacklist/<int:receiver_id>", methods=["DELETE"]
)
def delete_blacklist_entry_handler(gifter_id: int, receiver_id: int):
    try:
        delete_blacklist_entry.perform(gifter_id, receiver_id)

        return "", 204

    except UnknownParticipantError:
        return jsonify({"error": "Unknown participant"}), 400
    except BlacklistNotFoundError:
        return jsonify({"error": "Blacklist entry does not exist"}), 404
