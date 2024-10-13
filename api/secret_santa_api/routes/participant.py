from flask import Blueprint, jsonify

from secret_santa_api.registry import get_all_participants

participant_bp = Blueprint("participant", __name__, url_prefix="/participants")


@participant_bp.route("/", methods=["GET"])
def get_participants():
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
