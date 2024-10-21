import datetime

from secret_santa_api.db import db
from secret_santa_api.domain.entities.participant import (
    Participant as ParticipantEntity,
)
from secret_santa_api.infrastructure.adapters.database.participant import (
    Participant as ParticipantDB,
)
from secret_santa_api.infrastructure.adapters.draw import DrawRepositorySQLAdapter


class TestDrawRepositorySQLAdapter:
    draw_adapter = DrawRepositorySQLAdapter()

    def test_save(self, app_context):
        participant_1_db = ParticipantDB(name="Pierre", email="pierre@fr.fr")
        participant_2_db = ParticipantDB(name="Paul", email="paul@fr.fr")
        participant_3_db = ParticipantDB(name="Jacques", email="jacques@fr.fr")

        db.session.add(participant_1_db)
        db.session.add(participant_2_db)
        db.session.add(participant_3_db)
        db.session.commit()
        db.session.refresh(participant_1_db)
        db.session.refresh(participant_2_db)
        db.session.refresh(participant_3_db)

        participant_1 = ParticipantEntity(
            id=participant_1_db.id,
            name="Pierre",
            email="pierre@fr.fr",
            created=datetime.datetime.now(datetime.timezone.utc),
        )
        participant_2 = ParticipantEntity(
            id=participant_2_db.id,
            name="Paul",
            email="paul@fr.fr",
            created=datetime.datetime.now(datetime.timezone.utc),
        )
        participant_3 = ParticipantEntity(
            id=participant_3_db.id,
            name="Jacques",
            email="jacques@fr.fr",
            created=datetime.datetime.now(datetime.timezone.utc),
        )

        draw_details = [
            (participant_1, participant_2),
            (participant_3, participant_1),
            (participant_2, participant_3),
        ]

        draw = self.draw_adapter.save(draw_details)

        assert draw.id is not None
        assert len(draw.details) == len(draw_details)
