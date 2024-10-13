from unittest.mock import MagicMock

import pytest

from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.errrors import ParticipantAlreadyRegisteredError
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort
from secret_santa_api.domain.use_cases.add_participant import AddParticipant


class TestAddParticipant:
    def test_perform_with_used_email_raises_error(self):
        new_participant = Participant(name="FFFF", email="toto@mail.com")
        existing_participant = Participant(id=1000, name="FFFF", email="toto@mail.com")

        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_email.return_value = existing_participant

        add_participant = AddParticipant(participant_repository_mock)

        with pytest.raises(ParticipantAlreadyRegisteredError):
            add_participant.perform(new_participant)

        assert participant_repository_mock.save.call_count == 0

    def test_perform_with_return_participant(self):
        new_participant = Participant(name="FFFF", email="tata@mail.com")
        created_participant = Participant(id=1000, name="FFFF", email="toto@mail.com")

        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_email.return_value = None
        participant_repository_mock.save.return_value = created_participant

        add_participant = AddParticipant(participant_repository_mock)
        actual_participant = add_participant.perform(new_participant)

        assert created_participant == actual_participant
