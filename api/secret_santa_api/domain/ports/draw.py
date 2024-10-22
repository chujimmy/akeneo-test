from abc import ABC, abstractmethod
from typing import List

from secret_santa_api.domain.entities.draw import Draw
from secret_santa_api.domain.entities.participant import Participant


class DrawRepositoryPort(ABC):
    @abstractmethod
    def save(self, draw: List[tuple[Participant, Participant]]) -> Draw:
        pass

    @abstractmethod
    def get_latest_draws(self, limit: int) -> List[Draw]:
        pass
