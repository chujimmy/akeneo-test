import datetime
from unittest import mock
from unittest.mock import MagicMock

import pytest

from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.errrors import UnknownParticipantError
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort
from secret_santa_api.domain.use_cases.delete_blacklist_entry import (
    DeleteBlacklistEntry,
)


class TestDeleteBlacklistEntry:
    def test_perform_with_unknown_gifter_raises_error(self):
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_id.return_value = None

        delete_blacklist_entry = DeleteBlacklistEntry(participant_repository_mock)

        with pytest.raises(UnknownParticipantError):
            delete_blacklist_entry.perform(1, 2)

        assert participant_repository_mock.find_by_id.call_count == 1
        assert participant_repository_mock.find_by_id.call_args_list == [mock.call(1)]
        assert participant_repository_mock.delete_blacklist_entry.call_count == 0

    def test_perform_with_unknown_receiver_raises_error(self):
        created = datetime.datetime.now(datetime.timezone.utc)

        gifter = Participant(id=1, name="Name", email="t@m.fr", created=created)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_id.side_effect = lambda id: (
            None if id == 2 else gifter
        )

        delete_blacklist_entry = DeleteBlacklistEntry(participant_repository_mock)

        with pytest.raises(UnknownParticipantError):
            delete_blacklist_entry.perform(1, 2)

        assert participant_repository_mock.find_by_id.call_count == 2
        assert participant_repository_mock.find_by_id.call_args_list == [
            mock.call(1),
            mock.call(2),
        ]
        assert participant_repository_mock.delete_blacklist_entry.call_count == 0

    def test_perform(self):
        created = datetime.datetime.now(datetime.timezone.utc)
        gifter = Participant(id=1, name="Name", email="t@m.fr", created=created)
        recevier = Participant(id=2, name="X", email="x@m.fr", created=created)

        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.find_by_id.side_effect = lambda id: (
            recevier if id == 2 else gifter
        )

        delete_blacklist_entry = DeleteBlacklistEntry(participant_repository_mock)

        delete_blacklist_entry.perform(1, 2)

        assert participant_repository_mock.find_by_id.call_count == 2
        assert participant_repository_mock.delete_blacklist_entry.call_count == 1
        assert participant_repository_mock.delete_blacklist_entry.call_args_list == [
            mock.call(gifter, recevier)
        ]
