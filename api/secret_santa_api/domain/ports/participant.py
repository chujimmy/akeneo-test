from abc import ABC, abstractmethod
from typing import List, Optional

from secret_santa_api.domain.entities.participant import Participant


class ParticipantRepositoryPort(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Participant]:
        pass

    @abstractmethod
    def save(self, participent: Participant) -> Participant:
        pass

    @abstractmethod
    def get_all_participants(self) -> List[Participant]:
        pass
