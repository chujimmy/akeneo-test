from dataclasses import dataclass
from typing import Optional


@dataclass
class Participant:
    name: str
    email: str
    id: Optional[int] = None
