"""
test_notifications.py  –  v0.2
These tests map 1-to-1 to the numbered teacher bullets.
"""

from notifications import NotificationService
import time

def _fresh():
    return NotificationService(storage_path=":memory:")

def test_01_refresh_adds_new_items():
    s = _fresh()
    s.refresh(n_fake=3)
    assert len(s.list()) == 3

def test_02_chronological_sorting():
    s = _fresh()
    s.refresh(n_fake=5)
    ts = [n.timestamp for n in s.list()]
    assert ts == sorted(ts)

def test_03_filter_by_category():
    s = _fresh(); s.refresh(n_fake=20)
    offers = s.list(category="offers")
    assert all(n.category == "offers" for n in offers)

def test_04_unread_only_flag():
    s = _fresh(); s.refresh()
    nid = s.list()[0].id
    s.mark_read(nid)
    assert len(s.list(unread_only=True)) == 0

def test_05_mark_read_changes_state():
    s = _fresh(); s.refresh()
    nid = s.list()[0].id
    s.mark_read(nid)
    assert s.list()[0].read is True

def test_06_delete_removes_item():
    s = _fresh(); s.refresh()
    nid = s.list()[0].id
    s.delete(nid)
    assert len(s.list()) == 0
