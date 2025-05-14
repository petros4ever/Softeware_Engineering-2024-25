"""
Notification module – use-case «Ειδοποιήσεις»

Author: Kourtis Konstantinos (ΑΜ 1072613)
Created: 2025-05-13 • Last edit: 2025-05-14 (v0.2)
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Literal
import json, pathlib, random

Category = Literal["offers", "community", "requests"]


@dataclass
class Notification:
    id: int
    category: Category
    title: str
    content: str
    timestamp: datetime
    read: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d

    @staticmethod
    def from_dict(d: dict) -> "Notification":
        return Notification(**{**d, "timestamp": datetime.fromisoformat(d["timestamp"])})
    # ──────────────────────────────────────────────────────────────────────────────


class NotificationService:
    """
    CRUD + filtering.  JSON persistence by default, ':memory:' for fast tests.
    """

    def __init__(self, storage_path: str | pathlib.Path = "notifications.json"):
        self.memory_only = storage_path == ":memory:"
        self.storage_path = None if self.memory_only else pathlib.Path(storage_path)
        self._notifications: List[Notification] = []
        self._load()

    # ───────── internal helpers ────────────────────────────────────────────────
    def _load(self) -> None:
        if self.memory_only:
            return
        if self.storage_path and self.storage_path.exists():
            self._notifications = [
                Notification.from_dict(d)
                for d in json.loads(self.storage_path.read_text(encoding="utf-8"))
            ]

    def _save(self) -> None:
        if self.memory_only or not self.storage_path:
            return
        self.storage_path.write_text(
            json.dumps([n.to_dict() for n in self._notifications], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _next_id(self) -> int:
        return max((n.id for n in self._notifications), default=0) + 1

    # ───────── public API (maps 1-to-1 with UC steps) ──────────────────────────
    def refresh(self, *, n_fake: int = 1) -> None:
        """
        Pull new offers / community updates from “server”.
        Step 2 & 14 of the basic flow.
        """
        now = datetime.now()
        for _ in range(n_fake):
            self._notifications.append(
                Notification(
                    id=self._next_id(),
                    category=random.choice(["offers", "community", "requests"]),
                    title="Νέα ειδοποίηση",
                    content="Δείγμα περιεχομένου.",
                    timestamp=now,
                )
            )
        self._save()

    def list(
        self,
        *,
        category: Optional[Category] = None,
        unread_only: bool = False,
    ) -> List[Notification]:
        items = sorted(self._notifications, key=lambda n: n.timestamp, reverse=False)
        if category:
            items = [n for n in items if n.category == category]
        if unread_only:
            items = [n for n in items if not n.read]
        return items

    def mark_read(self, nid: int) -> bool:
        trg = next((n for n in self._notifications if n.id == nid), None)
        if trg:
            trg.read = True
            self._save()
            return True
        return False

    def delete(self, nid: int) -> bool:
        before = len(self._notifications)
        self._notifications = [n for n in self._notifications if n.id != nid]
        if len(self._notifications) < before:
            self._save()
            return True
        return False
