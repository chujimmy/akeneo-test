import datetime

from secret_santa_api.domain.entities.draw import Draw
from secret_santa_api.domain.entities.participant import Participant


class TestDrawRoutes:
    def test_generate_draw_with_no_draw_possible_return_409(self, client, mocker):
        mocker.patch(
            "secret_santa_api.infrastructure.routes.draw.generate_draw.perform",
            return_value=None,
        )

        response = client.post("/draws/")

        assert response.status_code == 409
        assert response.json == {
            "error": "Impossible to create a draw based on the condition (not enough particiants or too many constraints)"
        }

    def test_generate_draw_with_draw_generated_return_201(self, client, mocker):
        participant_1 = Participant(
            id=1,
            name="John Doe",
            email="test@mail.com",
            created=datetime.datetime.now(datetime.timezone.utc),
        )
        participant_2 = Participant(
            id=2,
            name="Jane Doe",
            email="bonjour@mail.com",
            created=datetime.datetime.now(datetime.timezone.utc),
        )
        participant_3 = Participant(
            id=2,
            name="Jane Doe",
            email="salut@mail.com",
            created=datetime.datetime.now(datetime.timezone.utc),
        )

        details = [
            (participant_1, participant_2),
            (participant_2, participant_3),
            (participant_3, participant_1),
        ]
        draw = Draw(
            id=1,
            details=details,
            created=datetime.datetime(
                2024, 6, 1, 12, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
        )

        mocker.patch(
            "secret_santa_api.infrastructure.routes.draw.generate_draw.perform",
            return_value=draw,
        )

        expected_response = {
            "id": draw.id,
            "created": "2024-06-01T12:00:00Z",
            "details": [
                {
                    "gifter": {
                        "id": d[0].id,
                        "name": d[0].name,
                        "email": d[0].email,
                    },
                    "receiver": {
                        "id": d[1].id,
                        "name": d[1].name,
                        "email": d[1].email,
                    },
                }
                for d in draw.details
            ],
        }

        response = client.post("/draws/")

        assert response.status_code == 201
        assert response.json == expected_response
