from secret_santa_api.domain.entities.participant import Participant
from secret_santa_api.domain.errrors import ParticipantAlreadyRegisteredError
from secret_santa_api.domain.ports.participant import ParticipantRepositoryPort


class AddParticipant:
    def __init__(self, participant_repository_port: ParticipantRepositoryPort) -> None:
        self.participant_repository_port = participant_repository_port

    def perform(self, participant: Participant) -> Participant:
        existing_participant = self.participant_repository_port.find_by_email(
            participant.email
        )

        if existing_participant:
            raise ParticipantAlreadyRegisteredError()

        return self.participant_repository_port.save(participant)
