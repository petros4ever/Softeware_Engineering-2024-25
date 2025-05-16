


from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import json
import pathlib
import random


@dataclass
class Notification:
    """Domain object representing a single notification."""
    id: int
    category: str  # 'offers', 'community', 'requests'
    title: str
    content: str
    timestamp: datetime
    read: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "read": self.read,
        }

    @staticmethod
    def from_dict(d: dict) -> "Notification":
        return Notification(
            id=d["id"],
            category=d["category"],
            title=d["title"],
            content=d["content"],
            timestamp=datetime.fromisoformat(d["timestamp"]),
            read=d["read"],
        )


class NotificationService:
    """CRUD + filtering service for notifications."""

    def __init__(self, storage_path: str = "notifications.json"):
        self.memory_only = storage_path == ":memory:"
        self.storage_path = None if self.memory_only else pathlib.Path(storage_path)
        self._notifications: List[Notification] = []
        self._load()

    def _load(self) -> None:
        if self.memory_only:
            self._notifications = []
            return
        if self.storage_path.exists():
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self._notifications = [Notification.from_dict(n) for n in data]
        else:
            self._notifications = []
            self._save()

    def _save(self) -> None:
        if self.memory_only or not self.storage_path:
            return
        data = [n.to_dict() for n in self._notifications]
        self.storage_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _next_id(self) -> int:
        return 1 if not self._notifications else max(n.id for n in self._notifications) + 1

    def refresh(self, n_fake: int = 1) -> None:
        now = datetime.now()
        for _ in range(n_fake):
            dummy = Notification(id=self._next_id(), category=random.choice(["offers","community","requests"]),
                                 title="Νέα ειδοποίηση", content="Δείγμα...", timestamp=now)
            self._notifications.append(dummy)
        self._save()

    def list(self, category: Optional[str]=None, unread_only: bool=False) -> List[Notification]:
        items = sorted(self._notifications, key=lambda n: n.timestamp)
        if category: items = [n for n in items if n.category==category]
        if unread_only: items = [n for n in items if not n.read]
        return items

    def mark_read(self, notification_id: int) -> bool:
        for n in self._notifications:
            if n.id==notification_id:
                n.read=True
                self._save()
                return True
        return False

    def delete(self, notification_id: int) -> bool:
        before = len(self._notifications)
        self._notifications = [n for n in self._notifications if n.id!=notification_id]
        if len(self._notifications)<before:
            self._save()
            return True
        return False
