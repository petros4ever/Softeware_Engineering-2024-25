# notifications/__init__.py
from .notifications import NotificationService, Notification   # re-export   <-- add this
__all__ = ["NotificationService", "Notification"]             # optional
