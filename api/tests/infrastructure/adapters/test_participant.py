import datetime

from secret_santa_api.db import db
from secret_santa_api.domain.entities.participant import (
    Participant as ParticipantEntity,
)
from secret_santa_api.infrastructure.adapters.database.participant import (
    Blacklist as BlacklistDB,
    Participant as ParticipantDB,
)
from secret_santa_api.infrastructure.adapters.participant import (
    ParticipantRepositorySQLAdapter,
    to_participant_entity,
)


class TestParticipantRepositorySQLAdapter:
    participant_adapter = ParticipantRepositorySQLAdapter()

    def test_find_by_id_without_entry_returns_none(self, app_context):
        participant = self.participant_adapter.find_by_id(11)

        assert participant is None

    def test_find_by_id_returns_participant(self, app_context):
        participant_db = ParticipantDB(id=12222, name="Max", email="max.power@mail.fr")

        db.session.add(participant_db)
        db.session.commit()

        participant = self.participant_adapter.find_by_id(12222)

        assert participant.id == participant_db.id
        assert participant.email == participant_db.email

    def test_find_by_email_without_entry_returns_none(self, app_context):
        participant = self.participant_adapter.find_by_email("toto@gg.com")

        assert participant is None

    def test_find_by_email_returns_participant(self, app_context):
        participant_db = ParticipantDB(id=1, name="Max", email="max.power@mail.fr")

        db.session.add(participant_db)
        db.session.commit()

        actual_participant = self.participant_adapter.find_by_email("max.power@mail.fr")

        assert actual_participant.id == participant_db.id
        assert actual_participant.name == participant_db.name
        assert actual_participant.email == participant_db.email

    def test_save(self, app_context):
        participant_to_save = ParticipantEntity(
            name="Lando",
            email="lando@mcl.fr",
            created=datetime.datetime.now(datetime.timezone.utc),
        )

        saved_participant = self.participant_adapter.save(participant_to_save)

        assert saved_participant.id is not None
        assert saved_participant.name == participant_to_save.name
        assert saved_participant.email == participant_to_save.email

    def test_get_all_participants_returns_participants(self, app_context):
        participant = ParticipantDB(
            id=100, name="Max Power", email="max.power@mail.com"
        )

        db.session.add(participant)
        db.session.commit()

        participants = self.participant_adapter.get_all_participants()

        assert len(participants) == 1
        assert participants[0].id == participant.id
        assert participants[0].name == participant.name
        assert participants[0].email == participant.email

    def test_get_all_participants_with_empty_table_returns_empty_list(
        self, app_context
    ):
        participants = self.participant_adapter.get_all_participants()

        assert participants == []

    def test_does_blacklist_exist_with_existing_one_returns_true(self, app_context):
        gifter_db = ParticipantDB(id=1, name="Max", email="max.power@mail.fr")
        receiver_db = ParticipantDB(id=2, name="Alice", email="alice@mail.fr")

        blacklist_db = BlacklistDB(gifter_id=gifter_db.id, receiver_id=receiver_db.id)

        db.session.add(gifter_db)
        db.session.add(receiver_db)
        db.session.add(blacklist_db)
        db.session.commit()

        blacklist_exists = self.participant_adapter.does_blacklist_exist(
            to_participant_entity(gifter_db),
            to_participant_entity(receiver_db),
        )

        assert blacklist_exists is True

    def test_does_blacklist_exist_without_existing_one_returns_false(self, app_context):
        gifter_db = ParticipantDB(id=1, name="Max", email="max.power@mail.fr")
        receiver_db = ParticipantDB(id=2, name="Alice", email="alice@mail.fr")

        db.session.add(gifter_db)
        db.session.add(receiver_db)
        db.session.commit()

        blacklist_exists = self.participant_adapter.does_blacklist_exist(
            to_participant_entity(gifter_db),
            to_participant_entity(receiver_db),
        )

        assert blacklist_exists is False
