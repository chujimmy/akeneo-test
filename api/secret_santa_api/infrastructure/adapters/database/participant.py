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
        server_default=func.strftime("%Y-%m-%dT%H:%M:%fZ"),
    )

    # Relationship to blacklist
    blacklisted_by = db.relationship(
        "Blacklist",
        backref="receiver",
        foreign_keys="[Blacklist.receiver_id]",
    )
    blacklisting = db.relationship(
        "Blacklist",
        backref="gifter",
        foreign_keys="[Blacklist.gifter_id]",
    )


class Blacklist(db.Model):  # type: ignore
    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gifter_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.strftime("%Y-%m-%dT%H:%M:%fZ"),
    )

    __table_args__ = (
        db.UniqueConstraint(
            "gifter_id", "receiver_id", name="blacklist_unique_gifter_receiver"
        ),
    )
