from sqlalchemy.sql import func

from secret_santa_api.db import db


class Draw(db.Model):  # type: ignore
    __tablename__ = "draw"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.strftime("%Y-%m-%dT%H:%M:%SZ", func.datetime("now", "utc")),
    )

    details = db.relationship("DrawDetail", back_populates="draw")


class DrawDetail(db.Model):  # type: ignore
    __tablename__ = "draw_detail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    draw_id = db.Column(db.Integer, db.ForeignKey("draw.id"))
    gifter_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("participant.id"))

    draw = db.relationship("Draw", back_populates="details")
    gifter = db.relationship("Participant", foreign_keys=[gifter_id])
    receiver = db.relationship("Participant", foreign_keys=[receiver_id])
