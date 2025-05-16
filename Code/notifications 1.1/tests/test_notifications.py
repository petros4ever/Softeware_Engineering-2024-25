import pytest
from notifications.notifications import NotificationService, Notification
from datetime import datetime

def test_refresh():
    svc = NotificationService(storage_path=":memory:")
    svc.refresh()
    assert svc.list()

def test_mark_read():
    svc = NotificationService(storage_path=":memory:")
    svc.refresh()
    nid = svc.list()[0].id
    svc.mark_read(nid)
    assert svc.list()[0].read

def test_delete():
    svc = NotificationService(storage_path=":memory:")
    svc.refresh(n_fake=2)
    ids = [n.id for n in svc.list()]
    svc.delete(ids[0])
    assert len(svc.list()) == 1
