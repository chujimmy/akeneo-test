from flask import Blueprint, jsonify

participant_bp = Blueprint("participant", __name__, url_prefix="/participants")


@participant_bp.route("/", methods=["GET"])
def get_participants():
    return jsonify({"participants": ["foo", "bar"]})
