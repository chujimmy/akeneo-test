from typing import List

from secret_santa_api.entities.participant import Participant
from secret_santa_api.ports.participant import ParticipantRepositoryPort


class GetAllParticipants:
    def __init__(self, participant_repository_port: ParticipantRepositoryPort) -> None:
        self.participant_repository_port = participant_repository_port

    def perform(self) -> List[Participant]:
        return self.participant_repository_port.get_all_participants()
