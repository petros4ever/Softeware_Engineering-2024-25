"""Domain models for comment moderation."""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Comment:
    id: int
    user_id: int
    content: str
    timestamp: datetime
    deleted: bool = False

@dataclass
class Report:
    id: int
    comment_id: int
    reporter_id: int
    reason: str
    timestamp: datetime

@dataclass
class AdminNotification:
    id: int
    message: str
    timestamp: datetime
    read: bool = False
