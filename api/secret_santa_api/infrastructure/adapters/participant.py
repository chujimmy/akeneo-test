from typing import List, Optional

from secret_santa_api.db import db
from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort
from secret_santa_api.infrastructure.adapters.database.participant import (
    Participant as ParticipantDB,
)


def to_entity(participant_db: ParticipantDB) -> Participant:
    return Participant(
        id=participant_db.id,
        name=participant_db.name,
        email=participant_db.email,
        created=participant_db.date_created,
    )


class ParticipantRepositorySQLAdapter(ParticipantRepositoryPort):
    def find_by_email(self, email: str) -> Optional[Participant]:
        participant_db = ParticipantDB.query.filter(
            ParticipantDB.email == email
        ).first()

        if not participant_db:
            return None

        return to_entity(participant_db)

    def save(self, participant: Participant) -> Participant:
        participant_db = ParticipantDB(
            name=participant.name,
            email=participant.email,
            date_created=participant.created,
        )

        db.session.add(participant_db)
        db.session.commit()
        db.session.refresh(participant_db)

        return to_entity(participant_db)

    def get_all_participants(self) -> List[Participant]:
        participants_db = ParticipantDB.query.order_by(ParticipantDB.date_created).all()

        participants = [to_entity(p) for p in participants_db]

        return participants
