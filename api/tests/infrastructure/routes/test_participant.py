from datetime import datetime, timezone

from secret_santa_api.domain.entities.participant import Blacklist, Participant
from secret_santa_api.domain.errrors import (
    BlacklistAlreadyExistError,
    BlacklistNotFoundError,
    ParticipantAlreadyRegisteredError,
    UnknownParticipantError,
)


class TestParticipantRoutes:
    def test_get_participants_with_no_participant_returns_empty_participants(
        self, client, mocker
    ):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.get_all_participants.perform",
            return_value=[],
        )

        response = client.get("/participants/")

        assert response.status_code == 200
        assert response.json == {"participants": []}

    def test_get_participants_returns_participants(self, client, mocker):
        participants = [
            Participant(
                id=1,
                name="John Doe",
                email="test@mail.com",
                created=datetime(2024, 6, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
            ),
            Participant(
                id=2,
                name="Jane Doe",
                email="bonjour@mail.com",
                created=datetime(2024, 6, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
            ),
        ]

        expected_response = [
            {
                "id": p.id,
                "name": p.name,
                "email": p.email,
                "created": p.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "blacklist": [],
            }
            for p in participants
        ]

        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.get_all_participants.perform",
            return_value=participants,
        )

        response = client.get("/participants/")

        assert response.status_code == 200
        assert response.json == {"participants": expected_response}

    def test_add_participant_with_invalid_payload_returns_400(self, client, mocker):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.add_participant.perform",
            side_effect=ParticipantAlreadyRegisteredError,
        )

        response = client.post(
            "/participants/", json={"name": "M", "email": "not_an_email"}
        )

        assert response.status_code == 400

    def test_add_participant_with_used_email_returns_409(self, client, mocker):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.add_participant.perform",
            side_effect=ParticipantAlreadyRegisteredError,
        )

        response = client.post(
            "/participants/", json={"name": "M", "email": "test@test.fr"}
        )

        assert response.status_code == 409
        assert response.json == {"error": "Participant already registered (email used)"}

    def test_add_participant_returns_201(self, client, mocker):
        name = "Charles Leclerc"
        email = "charles.leclerc@ferrari.it"
        added_participant = Participant(
            id=1,
            name=name,
            email=email,
            created=datetime(2024, 6, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        )

        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.add_participant.perform",
            return_value=added_participant,
        )

        response = client.post("/participants/", json={"name": name, "email": email})

        assert response.status_code == 201
        assert response.json == {
            "id": 1,
            "name": name,
            "email": email,
            "created": "2024-06-01T12:00:00.000000Z",
        }

    def test_blacklist_participant_with_unknown_participant_returns_400(
        self, client, mocker
    ):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.blacklist_participant.perform",
            side_effect=UnknownParticipantError,
        )

        response = client.post("/participants/1/blacklist/2")

        assert response.status_code == 400
        assert response.json["error"] == "Unknown participant"

    def test_blacklist_participant_with_blacklist_already_created_returns_409(
        self, client, mocker
    ):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.blacklist_participant.perform",
            side_effect=BlacklistAlreadyExistError,
        )

        response = client.post("/participants/1/blacklist/2")

        assert response.status_code == 409
        assert response.json["error"] == "Blacklist already exist"

    def test_blacklist_participant_returns_201(self, client, mocker):
        gifter = Participant(
            id=1,
            name="John Doe",
            email="test@mail.com",
            created=datetime(2024, 6, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        )
        receiver = Participant(
            id=2,
            name="Jane Doe",
            email="bonjour@mail.com",
            created=datetime(2024, 6, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        )
        blacklist = Blacklist(
            id=1000,
            created=datetime(2024, 6, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
            gifter=gifter,
            receiver=receiver,
        )

        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.blacklist_participant.perform",
            return_value=blacklist,
        )

        response = client.post("/participants/1/blacklist/2")

        assert response.status_code == 201
        assert response.json == {
            "id": blacklist.id,
            "created": blacklist.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "gifter_id": blacklist.gifter.id,
            "receiver_id": blacklist.receiver.id,
        }

    def test_delete_blacklist_entry_with_unknown_participant_returns_400(
        self, client, mocker
    ):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.delete_blacklist_entry.perform",
            side_effect=UnknownParticipantError,
        )

        response = client.delete("/participants/1/blacklist/2")

        assert response.status_code == 400
        assert response.json["error"] == "Unknown participant"

    def test_delete_blacklist_entry_without_valid_blacklist_entry_returns_404(
        self, client, mocker
    ):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.delete_blacklist_entry.perform",
            side_effect=BlacklistNotFoundError,
        )

        response = client.delete("/participants/1/blacklist/2")

        assert response.status_code == 404
        assert response.json["error"] == "Blacklist entry does not exist"

    def test_delete_blacklist_entry_returns_204(self, client, mocker):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.participant.delete_blacklist_entry.perform",
            return_value=None,
        )

        response = client.delete("/participants/1/blacklist/2")

        assert response.status_code == 204
