from datetime import datetime, timedelta, timezone

from secret_santa_api.db import db
from secret_santa_api.infrastructure.adapters.database.draw import (
    Draw as DrawDB,
    DrawDetail as DrawDetailDB,
)
from secret_santa_api.infrastructure.adapters.database.participant import (
    Participant as ParticipantDB,
)
from secret_santa_api.infrastructure.adapters.draw import DrawRepositorySQLAdapter
from secret_santa_api.infrastructure.adapters.participant import (
    to_entity as to_entity_participant,
)


class TestDrawRepositorySQLAdapter:
    draw_adapter = DrawRepositorySQLAdapter()

    def test_save(self, app_context):
        now = datetime.now(timezone.utc)
        participant_1_db = ParticipantDB(
            name="Pierre", email="pierre@fr.fr", date_created=now - timedelta(days=1)
        )
        participant_2_db = ParticipantDB(
            name="Paul", email="paul@fr.fr", date_created=now - timedelta(days=2)
        )
        participant_3_db = ParticipantDB(
            name="Jacques", email="jacques@fr.fr", date_created=now - timedelta(days=3)
        )

        db.session.add(participant_1_db)
        db.session.add(participant_2_db)
        db.session.add(participant_3_db)
        db.session.commit()
        db.session.refresh(participant_1_db)
        db.session.refresh(participant_2_db)
        db.session.refresh(participant_3_db)

        participant_1 = to_entity_participant(participant_1_db)
        participant_2 = to_entity_participant(participant_2_db)
        participant_3 = to_entity_participant(participant_3_db)

        draw_details = [
            (participant_1, participant_2),
            (participant_3, participant_1),
            (participant_2, participant_3),
        ]

        draw = self.draw_adapter.save(draw_details)

        assert draw.id is not None
        assert len(draw.details) == len(draw_details)

    def test_get_latest_draws_with_no_draw_return_empty_list(self, app_context):
        draws = self.draw_adapter.get_latest_draws(100)

        assert draws == []

    def test_get_latest_draws_with_limit_lower_than_draw_return_draws(
        self, app_context
    ):
        now = datetime.now(timezone.utc)
        participant_1_db = ParticipantDB(
            name="Pierre", email="pierre@fr.fr", date_created=now - timedelta(days=1)
        )
        participant_2_db = ParticipantDB(
            name="Paul", email="paul@fr.fr", date_created=now - timedelta(days=2)
        )
        participant_3_db = ParticipantDB(
            name="Jacques", email="jacques@fr.fr", date_created=now - timedelta(days=3)
        )

        db.session.add(participant_1_db)
        db.session.add(participant_2_db)
        db.session.add(participant_3_db)
        db.session.commit()
        db.session.refresh(participant_1_db)
        db.session.refresh(participant_2_db)
        db.session.refresh(participant_3_db)

        participant_1 = to_entity_participant(participant_1_db)
        participant_2 = to_entity_participant(participant_2_db)
        participant_3 = to_entity_participant(participant_3_db)

        draw_1 = DrawDB(
            date_created=now - timedelta(days=100),
            details=[
                DrawDetailDB(gifter_id=participant_1.id, receiver_id=participant_2.id),
                DrawDetailDB(gifter_id=participant_3.id, receiver_id=participant_2.id),
                DrawDetailDB(gifter_id=participant_2.id, receiver_id=participant_3.id),
            ],
        )

        draw_2 = DrawDB(
            date_created=now,
            details=[
                DrawDetailDB(gifter_id=participant_3.id, receiver_id=participant_1.id),
                DrawDetailDB(gifter_id=participant_1.id, receiver_id=participant_2.id),
                DrawDetailDB(gifter_id=participant_2.id, receiver_id=participant_3.id),
            ],
        )

        db.session.add(draw_1)
        db.session.add(draw_2)
        db.session.commit()
        db.session.refresh(draw_1)
        db.session.refresh(draw_2)

        draws = self.draw_adapter.get_latest_draws(1)

        assert len(draws) == 1
        assert draws[0].id == draw_2.id
        assert draws[0].details == [
            (participant_3, participant_1),
            (participant_1, participant_2),
            (participant_2, participant_3),
        ]

    def test_get_latest_draws_return_draws(self, app_context):
        now = datetime.now(timezone.utc)
        participant_1_db = ParticipantDB(
            name="Pierre", email="pierre@fr.fr", date_created=now - timedelta(days=1)
        )
        participant_2_db = ParticipantDB(
            name="Paul", email="paul@fr.fr", date_created=now - timedelta(days=2)
        )
        participant_3_db = ParticipantDB(
            name="Jacques", email="jacques@fr.fr", date_created=now - timedelta(days=3)
        )

        db.session.add(participant_1_db)
        db.session.add(participant_2_db)
        db.session.add(participant_3_db)
        db.session.commit()
        db.session.refresh(participant_1_db)
        db.session.refresh(participant_2_db)
        db.session.refresh(participant_3_db)

        participant_1 = to_entity_participant(participant_1_db)
        participant_2 = to_entity_participant(participant_2_db)
        participant_3 = to_entity_participant(participant_3_db)

        draw_1 = DrawDB(
            date_created=now - timedelta(days=100),
            details=[
                DrawDetailDB(gifter_id=participant_1.id, receiver_id=participant_3.id),
                DrawDetailDB(gifter_id=participant_2.id, receiver_id=participant_1.id),
                DrawDetailDB(gifter_id=participant_3.id, receiver_id=participant_2.id),
            ],
        )

        draw_2 = DrawDB(
            date_created=now,
            details=[
                DrawDetailDB(gifter_id=participant_2.id, receiver_id=participant_3.id),
                DrawDetailDB(gifter_id=participant_1.id, receiver_id=participant_2.id),
                DrawDetailDB(gifter_id=participant_3.id, receiver_id=participant_1.id),
            ],
        )

        db.session.add(draw_1)
        db.session.add(draw_2)
        db.session.commit()
        db.session.refresh(draw_1)
        db.session.refresh(draw_2)

        draws = self.draw_adapter.get_latest_draws(100)

        assert len(draws) == 2
        assert draws[0].id == draw_2.id
        assert draws[0].details == [
            (participant_2, participant_3),
            (participant_1, participant_2),
            (participant_3, participant_1),
        ]
        assert draws[1].id == draw_1.id
        assert draws[1].details == [
            (participant_1, participant_3),
            (participant_2, participant_1),
            (participant_3, participant_2),
        ]
