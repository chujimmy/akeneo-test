from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, order=True)
class Participant:
    name: str
    email: str
    id: Optional[int] = None
