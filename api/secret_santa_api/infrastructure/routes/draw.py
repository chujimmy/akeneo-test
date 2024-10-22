from typing import Any, Dict

from environs import Env
from flask import Blueprint, jsonify, request

from secret_santa_api.domain.entities.draw import Draw
from secret_santa_api.registry import generate_draw, get_lastest_draws


env = Env()

DRAW_DEFAULT_LIMIT = env.int("DRAW_DEFAULT_LIMITenv", 5)


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

    return jsonify(build_draw_response(draw)), 201


@draw_bp.route("/", methods=["GET"])
def get_latest_draws_handler():
    try:
        latest_draws_count = int(request.args.get("limit", DRAW_DEFAULT_LIMIT))
    except ValueError:
        latest_draws_count = DRAW_DEFAULT_LIMIT

    draws = get_lastest_draws.perform(latest_draws_count)

    return (
        jsonify(
            {
                "draws": [build_draw_response(draw) for draw in draws],
            }
        ),
        200,
    )


def build_draw_response(draw: Draw) -> Dict[str, Any]:
    return {
        "id": draw.id,
        "created": draw.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "details": [
            {
                "gifter": {
                    "id": d[0].id,
                    "name": d[0].name,
                    "email": d[0].email,
                },
                "receiver": {
                    "id": d[1].id,
                    "name": d[1].name,
                    "email": d[1].email,
                },
            }
            for d in draw.details
        ],
    }
