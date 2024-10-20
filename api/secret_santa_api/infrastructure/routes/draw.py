from flask import Blueprint, jsonify

from secret_santa_api.registry import generate_draw


draw_bp = Blueprint("draw", __name__, url_prefix="/draws")


@draw_bp.route("/", methods=["POST"])
def generate_draw_handler():
    draw = generate_draw.perform()

    if draw is None:
        return (
            jsonify(
                {
                    "error": "Impossible to create a draw based on the condition (not enough particiants or too many constraints)"
                }
            ),
            409,
        )

    return (
        jsonify(
            {
                "id": draw.id,
                "details": [
                    {
                        "gifter": {
                            "id": d[0].id,
                            "name": d[0].name,
                            "email": d[0].email,
                        },
                        "recevier": {
                            "id": d[1].id,
                            "name": d[1].name,
                            "email": d[1].email,
                        },
                    }
                    for d in draw.details
                ],
            }
        ),
        201,
    )
