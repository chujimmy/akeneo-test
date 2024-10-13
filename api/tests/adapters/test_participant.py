from secret_santa_api.adapters.database.participant import Participant as ParticipantDB
from secret_santa_api.adapters.participant import ParticipantRepositorySQLAdapter
from secret_santa_api.db import db


class TestParticipantRepositorySQLAdapter:
    participant_adapter = ParticipantRepositorySQLAdapter()

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
