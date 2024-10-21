from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True, order=True)
class Participant:
    name: str
    email: str
    created: datetime
    id: Optional[int] = None
