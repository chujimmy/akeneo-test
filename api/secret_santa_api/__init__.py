from environs import Env
from flask import Flask
from flask_cors import CORS

import secret_santa_api.models  # noqa
from secret_santa_api.db import db
from secret_santa_api.routes.participant import participant_bp

env = Env()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secret_santa.db"
    app.register_blueprint(participant_bp)

    db.init_app(app)

    CORS(app, resources={r"*": {"origins": "http://localhost:5173"}})

    with app.app_context():
        db.create_all()

    return app
