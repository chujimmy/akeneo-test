from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set


@dataclass(frozen=True, order=True)
class Participant:
    name: str
    email: str
    created: datetime
    blacklist: Set[int] = field(default_factory=set, hash=False)
    id: Optional[int] = None


@dataclass(frozen=True, order=True)
class Blacklist:
    id: int
    created: datetime
    gifter: Participant
    receiver: Participant
