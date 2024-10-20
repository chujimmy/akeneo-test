from typing import List

from secret_santa_api.db import db
from secret_santa_api.domain.entities.draw import Draw
from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.ports.draw import DrawRepositoryPort
from secret_santa_api.infrastructure.adapters.database.draw import (
    Draw as DrawDB,
    DrawDetail as DrawDetailDB,
)
from secret_santa_api.infrastructure.adapters.participant import (
    to_entity as to_participant_entity,
)


def to_entity(draw_db: DrawDB) -> Draw:
    draw_details = [
        (to_participant_entity(detail.gifter), to_participant_entity(detail.receiver))
        for detail in draw_db.details  # type: ignore
    ]
    return Draw(id=draw_db.id, details=draw_details)


class DrawRepositorySQLAdapter(DrawRepositoryPort):
    def save(self, draw_details: List[tuple[Participant, Participant]]) -> Draw:
        draw_details_db = [
            (DrawDetailDB(gifter_id=d[0].id, receiver_id=d[1].id)) for d in draw_details
        ]
        draw_db = DrawDB(details=draw_details_db)

        db.session.add(draw_db)
        db.session.commit()
        db.session.refresh(draw_db)

        return to_entity(draw_db)
