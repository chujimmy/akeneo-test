import random
from unittest.mock import MagicMock

import pytest

from secret_santa_api.domain.entities.draw import Draw
from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.ports.draw import DrawRepositoryPort
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort
from secret_santa_api.domain.use_cases.generate_draw import GenerateDraw


class TestGenerateDraw:
    def test_perform_with_no_participant_returns_none(self):
        draw_repository_mock = MagicMock(spec=DrawRepositoryPort)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.get_all_participants.return_value = []

        generate_draw = GenerateDraw(participant_repository_mock, draw_repository_mock)

        draw = generate_draw.perform()

        assert draw is None
        assert draw_repository_mock.save.call_count == 0

    def test_perform_with_one_participant_returns_none(self):
        participant = Participant(id=1, name="Name", email="test@mail.com")

        draw_repository_mock = MagicMock(spec=DrawRepositoryPort)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)
        participant_repository_mock.get_all_participants.return_value = [participant]

        generate_draw = GenerateDraw(participant_repository_mock, draw_repository_mock)

        draw = generate_draw.perform()

        assert draw is None
        assert draw_repository_mock.save.call_count == 0

    def test_perform_with_two_participants_returns_saved_draw(self):
        # Make the randonmess deterministic
        random.seed(71)

        participant_1 = Participant(id=1, name="Bob", email="bob@mail.com")
        participant_2 = Participant(id=2, name="Alice", email="alice@mail.com")

        draw_repository_mock = MagicMock(spec=DrawRepositoryPort)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)

        participant_repository_mock.get_all_participants.return_value = [
            participant_1,
            participant_2,
        ]
        draw_repository_mock.save.return_value = Draw(
            id=11,
            details=[(participant_1, participant_2), (participant_2, participant_1)],
        )

        generate_draw = GenerateDraw(participant_repository_mock, draw_repository_mock)

        draw = generate_draw.perform()

        assert draw.id == 11
        assert len(draw.details) == 2
        assert draw.details == [
            (participant_1, participant_2),
            (participant_2, participant_1),
        ]
        assert draw_repository_mock.save.call_count == 1
        draw_repository_mock.save.assert_called_with(
            [
                (participant_1, participant_2),
                (participant_2, participant_1),
            ]
        )

    def test_make_draw_two_participants_returns_list_drawn_participants(self):
        # Make the randonmess deterministic
        random.seed(1)

        participant_1 = Participant(id=1, name="Name", email="test1@mail.com")
        participant_2 = Participant(id=2, name="Name", email="test2@mail.com")

        draw_repository_mock = MagicMock(spec=DrawRepositoryPort)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)

        generate_draw = GenerateDraw(participant_repository_mock, draw_repository_mock)

        draw = generate_draw.make_draw([participant_1, participant_2])

        assert len(draw) == 2
        assert set(draw) == {
            (participant_1, participant_2),
            (participant_2, participant_1),
        }

    def test_make_draw_three_participants_with_impossible_draw_raises_error(self):
        # Make the randonmess deterministic
        random.seed(1)

        participant_1 = Participant(id=1, name="Bob", email="bob@mail.com")
        participant_2 = Participant(id=2, name="Alice", email="alice@mail.com")
        participant_3 = Participant(id=3, name="Charlie", email="charlie@mail.com")

        draw_repository_mock = MagicMock(spec=DrawRepositoryPort)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)

        generate_draw = GenerateDraw(participant_repository_mock, draw_repository_mock)

        with pytest.raises(ValueError):
            generate_draw.make_draw([participant_1, participant_2, participant_3])

    def test_make_draw_four_participants_return_list_drawn_participants(self):
        # Make the randonmess deterministic
        random.seed(1)

        participant_1 = Participant(id=1, name="Bob", email="bob@mail.com")
        participant_2 = Participant(id=2, name="Alice", email="alice@mail.com")
        participant_3 = Participant(id=3, name="Charlie", email="charlie@mail.com")
        participant_4 = Participant(id=3, name="David", email="david@mail.com")

        draw_repository_mock = MagicMock(spec=DrawRepositoryPort)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)

        generate_draw = GenerateDraw(participant_repository_mock, draw_repository_mock)

        draw = generate_draw.make_draw(
            [participant_1, participant_2, participant_3, participant_4]
        )

        assert draw == [
            (participant_4, participant_1),
            (participant_1, participant_2),
            (participant_3, participant_4),
            (participant_2, participant_3),
        ]

    def test_make_draw_many_participants_returns_list_drawn_participants(self):
        # Make the randonmess deterministic
        random.seed(1)

        number_participants = 500
        participants = [
            Participant(id=i, name="Name", email=f"test{i}@mail.com")
            for i in range(0, number_participants)
        ]

        draw_repository_mock = MagicMock(spec=DrawRepositoryPort)
        participant_repository_mock = MagicMock(spec=ParticipantRepositoryPort)

        generate_draw = GenerateDraw(participant_repository_mock, draw_repository_mock)

        draw = generate_draw.make_draw(participants)

        unique_gifters = [t[0] for t in draw]
        unique_receivers = [t[1] for t in draw]
        any_draw_self = next(
            (True for draw_detail in draw if draw_detail[0] == draw_detail[1]),
            False,
        )

        assert len(draw) == number_participants
        assert len(unique_gifters) == number_participants
        assert len(unique_receivers) == number_participants
        assert not any_draw_self
