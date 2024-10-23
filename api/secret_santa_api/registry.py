from environs import Env

from secret_santa_api.domain.use_cases.add_participant import AddParticipant
from secret_santa_api.domain.use_cases.blacklist_participant import BlacklistParticipant
from secret_santa_api.domain.use_cases.delete_blacklist_entry import (
    DeleteBlacklistEntry,
)
from secret_santa_api.domain.use_cases.generate_draw import GenerateDraw
from secret_santa_api.domain.use_cases.get_all_participants import GetAllParticipants
from secret_santa_api.domain.use_cases.get_latest_draws import GetLatestDraws
from secret_santa_api.infrastructure.adapters.draw import DrawRepositorySQLAdapter
from secret_santa_api.infrastructure.adapters.participant import (
    ParticipantRepositorySQLAdapter,
)


env = Env()

# Adapters
draw_repository_sql_adapter = DrawRepositorySQLAdapter()
participant_repository_sql_adapter = ParticipantRepositorySQLAdapter()

# Use Cases
add_participant = AddParticipant(participant_repository_sql_adapter)
blacklist_participant = BlacklistParticipant(participant_repository_sql_adapter)
delete_blacklist_entry = DeleteBlacklistEntry(participant_repository_sql_adapter)
generate_draw = GenerateDraw(
    participant_repository_sql_adapter,
    draw_repository_sql_adapter,
    env.int("DRAW_RETRY_FACTOR", 3),
)
get_lastest_draws = GetLatestDraws(draw_repository_sql_adapter)
get_all_participants = GetAllParticipants(participant_repository_sql_adapter)
