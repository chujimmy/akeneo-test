from typing import List, Optional

from secret_santa_api.db import db
from secret_santa_api.domain.entities.participant import Blacklist, Participant
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort
from secret_santa_api.infrastructure.adapters.database.participant import (
    Blacklist as BlacklistDB,
    Participant as ParticipantDB,
)


def to_participant_entity(participant_db: ParticipantDB) -> Participant:
    return Participant(
        id=participant_db.id,
        name=participant_db.name,
        email=participant_db.email,
        created=participant_db.date_created,
    )


def to_blacklist_entity(blacklist_db: BlacklistDB) -> Blacklist:
    return Blacklist(
        id=blacklist_db.id,
        created=blacklist_db.date_created,
        gifter=to_participant_entity(blacklist_db.gifter),
        receiver=to_participant_entity(blacklist_db.receiver),
    )


class ParticipantRepositorySQLAdapter(ParticipantRepositoryPort):
    def find_by_id(self, participant_id: int) -> Optional[Participant]:
        participant_db = ParticipantDB.query.filter(
            ParticipantDB.id == participant_id
        ).first()

        if not participant_db:
            return None

        return to_participant_entity(participant_db)

    def find_by_email(self, email: str) -> Optional[Participant]:
        participant_db = ParticipantDB.query.filter(
            ParticipantDB.email == email
        ).first()

        if not participant_db:
            return None

        return to_participant_entity(participant_db)

    def save(self, participant: Participant) -> Participant:
        participant_db = ParticipantDB(
            name=participant.name,
            email=participant.email,
            date_created=participant.created,
        )

        db.session.add(participant_db)
        db.session.commit()
        db.session.refresh(participant_db)

        return to_participant_entity(participant_db)

    def get_all_participants(self) -> List[Participant]:
        participants_db = ParticipantDB.query.order_by(ParticipantDB.date_created).all()

        participants = [to_participant_entity(p) for p in participants_db]

        return participants

    def does_blacklist_exist(self, gifter: Participant, receiver: Participant) -> bool:
        blacklist = BlacklistDB.query.filter(
            BlacklistDB.gifter_id == gifter.id, BlacklistDB.receiver_id == receiver.id
        ).first()

        if blacklist:
            return True

        return False

    def blacklist_participant(
        self, gifter: Participant, receiver: Participant
    ) -> Blacklist:
        blacklist_db = BlacklistDB(gifter_id=gifter.id, receiver_id=receiver.id)

        db.session.add(blacklist_db)
        db.session.commit()
        db.session.refresh(blacklist_db)

        return to_blacklist_entity(blacklist_db)
