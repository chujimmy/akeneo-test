from secret_santa_api.domain.use_cases.add_participant import AddParticipant
from secret_santa_api.domain.use_cases.get_all_participants import GetAllParticipants
from secret_santa_api.infrastructure.adapters.participant import (
    ParticipantRepositorySQLAdapter,
)


# Adapters
participant_repository_sql_adapter = ParticipantRepositorySQLAdapter()

# Use Cases
add_participant = AddParticipant(participant_repository_sql_adapter)
get_all_participants = GetAllParticipants(participant_repository_sql_adapter)
