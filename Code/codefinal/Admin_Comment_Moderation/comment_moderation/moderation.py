"""Orchestrates deletion + notifications to admin & reporters."""
from .services import CommentService, ReportService, AdminNotificationService

class ModerationService:
    def __init__(
        self,
        comment_service: CommentService,
        report_service: ReportService,
        notification_service: AdminNotificationService,
    ):
        self.comment_svc = comment_service
        self.report_svc = report_service
        self.notif_svc  = notification_service

    def delete_and_notify(self, comment_id: int) -> bool:
        ok = self.comment_svc.delete(comment_id)
        if not ok:
            return False
        self.notif_svc.notify(f"Comment {comment_id} deleted successfully")
        # notify reporters
        for rpt in self.report_svc.list():
            if rpt.comment_id == comment_id:
                self.notif_svc.notify(
                    f"Reporter {rpt.reporter_id}: your report was processed"
                )
        return True
