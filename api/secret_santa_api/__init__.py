import json
import logging

from dotenv import load_dotenv
from environs import Env
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

import secret_santa_api.infrastructure.adapters.database  # noqa
from secret_santa_api.db import db
from secret_santa_api.infrastructure.routes.draw import draw_bp
from secret_santa_api.infrastructure.routes.participant import participant_bp




def create_app(config_file_path: str):
    load_dotenv(dotenv_path=config_file_path)

    env = Env()

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.errorhandler(Exception)(handle_error)
    app.config["SQLALCHEMY_DATABASE_URI"] = env.str("SQLALCHEMY_DATABASE_URI")
    app.register_blueprint(draw_bp)
    app.register_blueprint(participant_bp)

    db.init_app(app)

    CORS(app, resources={r"*": {"origins": "http://localhost:5173"}})

    with app.app_context():
        db.create_all()

    @app.errorhandler(HTTPException)
    def handle_werkzeug_http_exception(e):
        """Return JSON instead of HTML for HTTP errors."""

        response = e.get_response()
        response.content_type = "application/json"
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )

        return response

    return app


def handle_error(e):
    if isinstance(e, HTTPException):
        return e

    logging.error(e)

    response = {
        "error": "An unexpected error occurred",
    }

    return jsonify(response), 500
