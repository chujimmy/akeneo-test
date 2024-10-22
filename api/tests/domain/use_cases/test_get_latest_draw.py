from unittest.mock import MagicMock

from secret_santa_api.domain.ports.draw import DrawRepositoryPort
from secret_santa_api.domain.use_cases.get_latest_draws import GetLatestDraws


class TestGetLatestDraws:
    def test_perform(self):
        draw_repository_mock = MagicMock(spec=DrawRepositoryPort)
        draw_repository_mock.get_latest_draws.return_value = []
        limit = 25

        get_latest_draws = GetLatestDraws(draw_repository_mock)

        draw = get_latest_draws.perform(limit)

        assert draw == []
        draw_repository_mock.get_latest_draws.assert_called_with(limit)
