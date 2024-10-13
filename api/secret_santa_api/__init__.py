import logging

from environs import Env
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

import secret_santa_api.infrastructure.adapters.database  # noqa
from secret_santa_api.db import db
from secret_santa_api.infrastructure.routes.participant import participant_bp


env = Env()


def create_app():
    app = Flask(__name__)
    app.errorhandler(Exception)(handle_error)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secret_santa.db"
    app.register_blueprint(participant_bp)

    db.init_app(app)

    CORS(app, resources={r"*": {"origins": "http://localhost:5173"}})

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app


def handle_error(e):
    if isinstance(e, HTTPException):
        return e

    logging.error(e)

    response = {
        "error": "An unexpected error occurred",
    }

    return jsonify(response), 500
