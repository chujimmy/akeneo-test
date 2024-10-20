from dataclasses import dataclass
from typing import List

from secret_santa_api.domain.entities.participant import Participant


@dataclass(frozen=True, order=True)
class Draw:
    id: int
    details: List[tuple[Participant, Participant]]