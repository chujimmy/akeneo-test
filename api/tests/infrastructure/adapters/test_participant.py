from secret_santa_api.db import db
from secret_santa_api.domain.entities.participant import (
    Participant as ParticipantEntity,
)
from secret_santa_api.infrastructure.adapters.database.participant import (
    Participant as ParticipantDB,
)
from secret_santa_api.infrastructure.adapters.participant import (
    ParticipantRepositorySQLAdapter,
)


class TestParticipantRepositorySQLAdapter:
    participant_adapter = ParticipantRepositorySQLAdapter()

    def test_find_by_email_without_entry_returns_none(self, app):
        with app.app_context():
            participant = self.participant_adapter.find_by_email("toto@gg.com")

            assert participant is None

    def test_find_by_email_returns_participant(self, app):
        with app.app_context():
            participant_db = ParticipantDB(id=1, name="Max", email="max.power@mail.fr")

            db.session.add(participant_db)
            db.session.commit()

            actual_participant = self.participant_adapter.find_by_email(
                "max.power@mail.fr"
            )

            assert actual_participant.id == participant_db.id
            assert actual_participant.name == participant_db.name
            assert actual_participant.email == participant_db.email

    def test_save(self, app):
        with app.app_context():
            participant_to_save = ParticipantEntity(name="Lando", email="lando@mcl.fr")

            saved_participant = self.participant_adapter.save(participant_to_save)

            assert saved_participant.id is not None
            assert saved_participant.name == participant_to_save.name
            assert saved_participant.email == participant_to_save.email

    def test_get_all_participants_returns_participants(self, app):
        with app.app_context():
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

    def test_get_all_participants_with_empty_table_returns_empty_list(self, app):
        with app.app_context():
            participants = self.participant_adapter.get_all_participants()

            assert participants == []
