from secret_santa_api.domain.entities.participant import Blacklist
from secret_santa_api.domain.errrors import (
    BlacklistAlreadyExistError,
    UnknownParticipantError,
)
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort


class BlacklistParticipant:
    def __init__(self, participant_repository_port: ParticipantRepositoryPort) -> None:
        self.participant_repository_port = participant_repository_port

    def perform(self, gifter_id: int, receiver_id: int) -> Blacklist:
        gifter = self.participant_repository_port.find_by_id(gifter_id)
        if not gifter:
            raise UnknownParticipantError()

        receiver = self.participant_repository_port.find_by_id(receiver_id)
        if not receiver:
            raise UnknownParticipantError()

        if self.participant_repository_port.does_blacklist_exist(gifter, receiver):
            raise BlacklistAlreadyExistError()

        return self.participant_repository_port.blacklist_participant(gifter, receiver)
