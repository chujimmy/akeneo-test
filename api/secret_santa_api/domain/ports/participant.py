from abc import ABC, abstractmethod
from typing import List, Optional

from secret_santa_api.domain.entities.participant import Blacklist, Participant


class ParticipantRepositoryPort(ABC):
    @abstractmethod
    def find_by_id(self, participant_id: int) -> Optional[Participant]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Participant]:
        pass

    @abstractmethod
    def save(self, participent: Participant) -> Participant:
        pass

    @abstractmethod
    def get_all_participants(self) -> List[Participant]:
        pass

    @abstractmethod
    def does_blacklist_exist(self, gifter: Participant, receiver: Participant) -> bool:
        pass

    @abstractmethod
    def blacklist_participant(
        self, gifter: Participant, receiver: Participant
    ) -> Blacklist:
        pass
