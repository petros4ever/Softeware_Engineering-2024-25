"""Core services for comments, reports, and admin notifications."""
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .models import Comment, Report, AdminNotification

class CommentService:
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else None
        self._comments: List[Comment] = []
        self._load()

    def _load(self):
        if self.storage_path and self.storage_path.exists():
            data = json.loads(self.storage_path.read_text(encoding='utf-8'))
            self._comments = [
                Comment(**{**d, 'timestamp': datetime.fromisoformat(d['timestamp'])})
                for d in data
            ]

    def _save(self):
        if self.storage_path:
            dump = []
            for c in self._comments:
                d = asdict(c)
                d['timestamp'] = c.timestamp.isoformat()
                dump.append(d)
            self.storage_path.write_text(
                json.dumps(dump, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )

    def _next_id(self) -> int:
        return max((c.id for c in self._comments), default=0) + 1

    def publish(self, user_id: int, content: str) -> Comment:
        now = datetime.now()
        c = Comment(id=self._next_id(), user_id=user_id, content=content, timestamp=now)
        self._comments.append(c)
        self._save()
        return c

    def delete(self, comment_id: int) -> bool:
        for c in self._comments:
            if c.id == comment_id and not c.deleted:
                c.deleted = True
                self._save()
                return True
        return False

    def list(self, include_deleted: bool = False) -> List[Comment]:
        if include_deleted:
            return list(self._comments)
        return [c for c in self._comments if not c.deleted]

class AdminNotificationService:
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else None
        self._notes: List[AdminNotification] = []
        self._load()

    def _load(self):
        if self.storage_path and self.storage_path.exists():
            data = json.loads(self.storage_path.read_text(encoding='utf-8'))
            self._notes = [
                AdminNotification(**{**d, 'timestamp': datetime.fromisoformat(d['timestamp'])})
                for d in data
            ]

    def _save(self):
        if self.storage_path:
            dump = []
            for n in self._notes:
                d = asdict(n)
                d['timestamp'] = n.timestamp.isoformat()
                dump.append(d)
            self.storage_path.write_text(
                json.dumps(dump, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )

    def _next_id(self) -> int:
        return max((n.id for n in self._notes), default=0) + 1

    def notify(self, message: str) -> AdminNotification:
        now = datetime.now()
        n = AdminNotification(id=self._next_id(), message=message, timestamp=now)
        self._notes.append(n)
        self._save()
        return n

    def list(self, unread_only: bool = False) -> List[AdminNotification]:
        notes = sorted(self._notes, key=lambda n: n.timestamp)
        if unread_only:
            notes = [n for n in notes if not n.read]
        return notes

    def mark_read(self, note_id: int) -> bool:
        for n in self._notes:
            if n.id == note_id and not n.read:
                n.read = True
                self._save()
                return True
        return False

class ReportService:
    def __init__(
        self,
        comment_service: CommentService,
        notification_service: AdminNotificationService,
        storage_path: Optional[str] = None,
    ):
        self.comment_svc = comment_service
        self.notif_svc   = notification_service
        self.storage_path = Path(storage_path) if storage_path else None
        self._reports: List[Report] = []
        self._load()

    def _load(self):
        if self.storage_path and self.storage_path.exists():
            data = json.loads(self.storage_path.read_text(encoding='utf-8'))
            self._reports = [
                Report(**{**d, 'timestamp': datetime.fromisoformat(d['timestamp'])})
                for d in data
            ]

    def _save(self):
        if self.storage_path:
            dump = []
            for r in self._reports:
                d = asdict(r); d['timestamp'] = r.timestamp.isoformat()
                dump.append(d)
            self.storage_path.write_text(
                json.dumps(dump, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )

    def _next_id(self) -> int:
        return max((r.id for r in self._reports), default=0) + 1

    def report(self, comment_id: int, reporter_id: int, reason: str) -> Report:
        now = datetime.now()
        rpt = Report(
            id=self._next_id(),
            comment_id=comment_id,
            reporter_id=reporter_id,
            reason=reason,
            timestamp=now,
        )
        self._reports.append(rpt)
        self._save()
        self.notif_svc.notify(f"New report: comment {comment_id} — reason: {reason}")
        return rpt

    def list(self) -> List[Report]:
        return sorted(self._reports, key=lambda r: r.timestamp)
