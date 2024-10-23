from secret_santa_api.domain.errrors import UnknownParticipantError
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort


class DeleteBlacklistEntry:
    def __init__(self, participant_repository_port: ParticipantRepositoryPort) -> None:
        self.participant_repository_port = participant_repository_port

    def perform(self, gifter_id: int, receiver_id: int) -> None:
        gifter = self.participant_repository_port.find_by_id(gifter_id)
        if not gifter:
            raise UnknownParticipantError()

        receiver = self.participant_repository_port.find_by_id(receiver_id)
        if not receiver:
            raise UnknownParticipantError()

        return self.participant_repository_port.delete_blacklist_entry(gifter, receiver)
