from typing import List

from secret_santa_api.domain.entities.draw import Draw
from secret_santa_api.domain.ports.draw import DrawRepositoryPort


class GetLatestDraws:
    def __init__(
        self,
        draw_repository_port: DrawRepositoryPort,
    ) -> None:
        self.draw_repository_port = draw_repository_port

    def perform(self, limit: int) -> List[Draw]:
        return self.draw_repository_port.get_latest_draws(limit)
