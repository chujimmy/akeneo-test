from secret_santa_api.entities.participant import Participant


class TestParticipantRoutes:
    def test_get_participants_with_no_participant_returns_empty_participants(
        self, client, mocker
    ):
        mocker.patch(
            "secret_santa_api.routes.participant.get_all_participants.perform",
            return_value=[],
        )

        response = client.get("/participants/")

        assert response.status_code == 200
        assert response.json == {"participants": []}

    def test_get_participants_returns_participants(self, client, mocker):
        participants = [
            Participant(id=1, name="John Doe", email="test@mail.com"),
            Participant(id=2, name="Jane Doe", email="bonjour@mail.com"),
        ]

        expected_response = [
            {
                "id": p.id,
                "name": p.name,
                "email": p.email,
            }
            for p in participants
        ]

        mocker.patch(
            "secret_santa_api.routes.participant.get_all_participants.perform",
            return_value=participants,
        )

        response = client.get("/participants/")

        assert response.status_code == 200
        assert response.json == {"participants": expected_response}
