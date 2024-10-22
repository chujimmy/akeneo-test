import datetime

from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.errrors import ParticipantAlreadyRegisteredError


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
                created=datetime.datetime(
                    2024, 6, 1, 12, 0, 0, 0, tzinfo=datetime.timezone.utc
                ),
            ),
            Participant(
                id=2,
                name="Jane Doe",
                email="bonjour@mail.com",
                created=datetime.datetime(
                    2024, 6, 1, 12, 0, 0, 0, tzinfo=datetime.timezone.utc
                ),
            ),
        ]

        expected_response = [
            {
                "id": p.id,
                "name": p.name,
                "email": p.email,
                "created": p.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
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
            created=datetime.datetime(
                2024, 6, 1, 12, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
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
