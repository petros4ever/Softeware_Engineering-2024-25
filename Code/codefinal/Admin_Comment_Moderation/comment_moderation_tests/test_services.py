"""PyTest suite for services + moderation flow."""
import time
import pytest

from comment_moderation.models import Comment, Report, AdminNotification
from comment_moderation.services import CommentService, ReportService, AdminNotificationService
from comment_moderation.moderation import ModerationService

@pytest.fixture
def comment_svc(tmp_path):
    return CommentService(storage_path=str(tmp_path/"comments.json"))

@pytest.fixture
def notif_svc(tmp_path):
    return AdminNotificationService(storage_path=str(tmp_path/"notes.json"))

@pytest.fixture
def report_svc(comment_svc, notif_svc, tmp_path):
    return ReportService(
        comment_service=comment_svc,
        notification_service=notif_svc,
        storage_path=str(tmp_path/"reports.json")
    )

@pytest.fixture
def mod_svc(comment_svc, report_svc, notif_svc):
    return ModerationService(
        comment_service=comment_svc,
        report_service=report_svc,
        notification_service=notif_svc
    )

def test_publish_and_delete(comment_svc):
    c = comment_svc.publish(1, "Hello")
    assert c.id == 1 and not c.deleted
    assert comment_svc.delete(c.id)
    assert comment_svc.list() == []

def test_report_triggers_admin_notification(report_svc, comment_svc, notif_svc):
    c = comment_svc.publish(1, "Bad")
    rpt = report_svc.report(c.id, reporter_id=2, reason="Spam")
    notes = notif_svc.list()
    assert len(notes) == 1
    assert "New report" in notes[0].message

def test_reports_chronological(report_svc, comment_svc):
    c1 = comment_svc.publish(1, "A")
    r1 = report_svc.report(c1.id, reporter_id=2, reason="R1")
    time.sleep(0.01)
    c2 = comment_svc.publish(1, "B")
    r2 = report_svc.report(c2.id, reporter_id=3, reason="R2")
    assert [r.id for r in report_svc.list()] == [1,2]

def test_moderation_delete_and_notify(comment_svc, report_svc, notif_svc, mod_svc):
    c = comment_svc.publish(5, "X")
    report_svc.report(c.id, reporter_id=6, reason="Y")
    ok = mod_svc.delete_and_notify(c.id)
    assert ok
    msgs = [n.message for n in notif_svc.list()]
    assert len(msgs) == 3
    assert "deleted successfully" in msgs[1]
    assert "report was processed" in msgs[2]
