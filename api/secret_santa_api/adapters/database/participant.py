from sqlalchemy.sql import func

from secret_santa_api.db import db


class Participant(db.Model):  # type: ignore
    __tablename__ = "participant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.strftime("%Y-%m-%dT%H:%M:%SZ", func.datetime("now", "utc")),
    )
