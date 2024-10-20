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
        participant_1 = Participant(id=1, name="John Doe", email="test@mail.com")
        participant_2 = Participant(id=2, name="Jane Doe", email="bonjour@mail.com")
        participant_3 = Participant(id=2, name="Jane Doe", email="salut@mail.com")

        details = [
            (participant_1, participant_2),
            (participant_2, participant_3),
            (participant_3, participant_1),
        ]
        draw = Draw(id=1, details=details)

        mocker.patch(
            "secret_santa_api.infrastructure.routes.draw.generate_draw.perform",
            return_value=draw,
        )

        expected_response = {
            "id": draw.id,
            "details": [
                {
                    "gifter": {
                        "id": d[0].id,
                        "name": d[0].name,
                        "email": d[0].email,
                    },
                    "recevier": {
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
