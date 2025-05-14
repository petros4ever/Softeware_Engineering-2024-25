"""Tkinter Admin Panel for comment moderation."""
import tkinter as tk
from tkinter import ttk, messagebox
import random  # 1) simulate new data on refresh

from .services import CommentService, AdminNotificationService, ReportService
from .moderation import ModerationService

class AdminPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Panel – Comment Moderation")
        self.geometry("900x500")

        self.comment_svc = CommentService()
        self.notif_svc   = AdminNotificationService()
        self.report_svc  = ReportService(self.comment_svc, self.notif_svc)
        self.mod_svc     = ModerationService(self.comment_svc, self.report_svc, self.notif_svc)

        # demo data
        c = self.comment_svc.publish(user_id=42, content="Suspicious comment")
        self.report_svc.report(c.id, reporter_id=7, reason="Offensive")

        self._build_ui()
        self._refresh_all()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        # ── Admin Notifications ────────────────────────────
        nf = ttk.Labelframe(paned, text="Admin Notifications")
        paned.add(nf, weight=1)
        cols = ("id", "message", "time", "read")
        self.tree_notif = ttk.Treeview(nf, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree_notif.heading(c, text=c.capitalize())
            self.tree_notif.column(c, width=120 if c=="id" else 200, anchor="w")
        self.tree_notif.pack(fill="both", expand=True, padx=5, pady=5)

        btnf = ttk.Frame(nf); btnf.pack(fill="x", pady=4)
        ttk.Button(btnf, text="Mark Read", command=self._mark_read).pack(side="left", padx=5)
        # 2) Refresh now calls our new _on_refresh
        ttk.Button(btnf, text="Refresh",   command=self._on_refresh).pack(side="right", padx=5)

        # ── Reported Comments ──────────────────────────────
        rf = ttk.Labelframe(paned, text="Reported Comments")
        paned.add(rf, weight=1)
        cols2 = ("id", "comment", "reporter", "reason", "time")
        self.tree_rep = ttk.Treeview(rf, columns=cols2, show="headings", height=15)
        for c in cols2:
            self.tree_rep.heading(c, text=c.capitalize())
            self.tree_rep.column(c, width=100 if c in ("id","comment","reporter") else 180, anchor="w")
        self.tree_rep.pack(fill="both", expand=True, padx=5, pady=5)
        ttk.Button(rf, text="Details & Delete", command=self._handle_delete).pack(pady=6)

    def _on_refresh(self):
        # 3a) simulate new incoming comment & report
        new_comment = self.comment_svc.publish(
            user_id=random.randint(1,100),
            content="Auto comment via Refresh"
        )
        self.report_svc.report(
            comment_id=new_comment.id,
            reporter_id=random.randint(1,100),
            reason="Auto-refresh"
        )
        # 3b) then reload both panes
        self._refresh_all()

    def _refresh_notif(self):
        for iid in self.tree_notif.get_children():
            self.tree_notif.delete(iid)
        for n in self.notif_svc.list():
            self.tree_notif.insert(
                "", "end", iid=n.id,
                values=(n.id, n.message, n.timestamp.strftime("%H:%M:%S"), "Yes" if n.read else "No")
            )

    def _refresh_reports(self):
        for iid in self.tree_rep.get_children():
            self.tree_rep.delete(iid)
        active_ids = {c.id for c in self.comment_svc.list(include_deleted=False)}
        for r in self.report_svc.list():
            if r.comment_id not in active_ids:
                continue
            self.tree_rep.insert(
                "", "end", iid=r.id,
                values=(r.id, r.comment_id, r.reporter_id, r.reason, r.timestamp.strftime("%H:%M:%S"))
            )

    def _refresh_all(self):
        self._refresh_notif()
        self._refresh_reports()

    def _mark_read(self):
        sel = self.tree_notif.selection()
        if sel:
            self.notif_svc.mark_read(int(sel[0]))
            self._refresh_notif()

    def _handle_delete(self):
        sel = self.tree_rep.selection()
        if not sel:
            return
        rid = int(sel[0])
        rpt = next(r for r in self.report_svc.list() if r.id == rid)
        comm = next(c for c in self.comment_svc.list(include_deleted=True) if c.id == rpt.comment_id)
        detail = (
            f"Comment #{comm.id}\n"
            f"User: {comm.user_id}\n"
            f"Content: {comm.content}\n\n"
            f"Reason: {rpt.reason}"
        )
        if messagebox.askyesno("Delete comment?", detail):
            self.mod_svc.delete_and_notify(comm.id)
            self._refresh_all()

if __name__ == "__main__":
    AdminPanel().mainloop()
