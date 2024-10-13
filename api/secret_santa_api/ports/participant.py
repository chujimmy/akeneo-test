from abc import ABC, abstractmethod
from typing import List

from secret_santa_api.entities.participant import Participant


class ParticipantRepositoryPort(ABC):
    @abstractmethod
    def get_all_participants(self) -> List[Participant]:
        pass
