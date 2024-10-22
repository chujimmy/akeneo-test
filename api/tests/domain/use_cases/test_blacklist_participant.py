import datetime
from unittest import mock
from unittest.mock import MagicMock

import pytest

from secret_santa_api.domain.entities.participant import Blacklist, Participant
from secret_santa_api.domain.errrors import (
    BlacklistAlreadyExistError,
    UnknownParticipantError,
)
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort
from secret_santa_api.domain.use_cases.blacklist_participant import BlacklistParticipant


class TestBlacklistParticipant:
    def test_perform_with_unknown_gifter_raises_error(self):
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_id.return_value = None

        blacklist_participant = BlacklistParticipant(participant_repository_mock)

        with pytest.raises(UnknownParticipantError):
            blacklist_participant.perform(1, 2)

        assert participant_repository_mock.does_blacklist_exist.call_count == 0
        assert participant_repository_mock.find_by_id.call_args_list == [mock.call(1)]
        assert participant_repository_mock.blacklist_participant.call_count == 0
        assert participant_repository_mock.find_by_id.call_count == 1

    def test_perform_with_unknown_receiver_raises_error(self):
        created = datetime.datetime.now(datetime.timezone.utc)

        gifter = Participant(id=1, name="Name", email="t@m.fr", created=created)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_id.side_effect = lambda id: (
            None if id == 2 else gifter
        )

        blacklist_participant = BlacklistParticipant(participant_repository_mock)

        with pytest.raises(UnknownParticipantError):
            blacklist_participant.perform(1, 2)

        assert participant_repository_mock.find_by_id.call_count == 2
        assert participant_repository_mock.find_by_id.call_args_list == [
            mock.call(1),
            mock.call(2),
        ]
        assert participant_repository_mock.does_blacklist_exist.call_count == 0
        assert participant_repository_mock.blacklist_participant.call_count == 0

    def test_perform_with_existing_blacklist_raises_error(self):
        created = datetime.datetime.now(datetime.timezone.utc)

        gifter = Participant(id=1, name="Name", email="t@m.fr", created=created)
        recevier = Participant(id=2, name="X", email="x@m.fr", created=created)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_id.side_effect = lambda id: (
            recevier if id == 2 else gifter
        )
        participant_repository_mock.does_blacklist_exist.return_value = True

        blacklist_participant = BlacklistParticipant(participant_repository_mock)

        with pytest.raises(BlacklistAlreadyExistError):
            blacklist_participant.perform(1, 2)

        assert participant_repository_mock.find_by_id.call_count == 2
        assert participant_repository_mock.does_blacklist_exist.call_count == 1
        assert participant_repository_mock.blacklist_participant.call_count == 0

    def test_perform_returns_blacklist(self):
        created = datetime.datetime.now(datetime.timezone.utc)
        gifter = Participant(id=1, name="Name", email="t@m.fr", created=created)
        recevier = Participant(id=2, name="X", email="x@m.fr", created=created)
        blacklist = Blacklist(id=111, created=created, gifter=gifter, receiver=recevier)

        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_id.side_effect = lambda id: (
            recevier if id == 2 else gifter
        )
        participant_repository_mock.does_blacklist_exist.return_value = False
        participant_repository_mock.blacklist_participant.return_value = blacklist

        blacklist_participant = BlacklistParticipant(participant_repository_mock)

        blacklist = blacklist_participant.perform(1, 2)

        assert participant_repository_mock.find_by_id.call_count == 2
        assert participant_repository_mock.does_blacklist_exist.call_count == 1
        assert participant_repository_mock.blacklist_participant.call_count == 1
        assert participant_repository_mock.blacklist_participant.call_args_list == [
            mock.call(gifter, recevier)
        ]
