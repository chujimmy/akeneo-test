from typing import List

from secret_santa_api.adapters.database.participant import Participant as ParticipantDB
from secret_santa_api.entities.participant import Participant
from secret_santa_api.ports.participant import ParticipantRepositoryPort


class ParticipantRepositorySQLAdapter(ParticipantRepositoryPort):
    def get_all_participants(self) -> List[Participant]:
        participants_db = ParticipantDB.query.order_by(ParticipantDB.date_created).all()

        participants = [
            Participant(id=p.id, name=p.name, email=p.email) for p in participants_db
        ]

        return participants
