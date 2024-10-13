from unittest.mock import MagicMock

from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort
from secret_santa_api.domain.use_cases.get_all_participants import GetAllParticipants


class TestGetAllParticipants:
    def test_perform_should_return_participants(self):
        participants = [
            Participant(id=10, name="Name", email="mail@mail.com"),
            Participant(id=20, name="FFFF", email="toto@mail.com"),
        ]
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.get_all_participants.return_value = participants
        get_all_participants = GetAllParticipants(participant_repository_mock)

        actual_participants = get_all_participants.perform()

        assert actual_participants == participants
