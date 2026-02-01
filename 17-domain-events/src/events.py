from dataclasses import dataclass
from datetime import datetime
from src.bus import DomainEvent


@dataclass
class UserRegistered(DomainEvent):
    user_id: int
    username: str
    email: str
    occurred_at: datetime = datetime.now()
