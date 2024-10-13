from datetime import datetime, timezone

from secret_santa_api.db import db

class Participant(db.Model): # type: ignore
    __tablename__ = "participant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
