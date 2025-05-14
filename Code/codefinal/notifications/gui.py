"""
Tkinter GUI for «Ειδοποιήσεις»

maps every bullet of the teacher’s basic flow.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from notifications import NotificationService
import notifications_settings as ns


class NotificationApp(tk.Tk):
    def __init__(self, service: NotificationService):
        super().__init__()
        self.service = service
        self.title("Ειδοποιήσεις")
        self.geometry("750x480")
        self._build()

    # ───────── UI layout ───────────────────────────────────────────────────────
    def _build(self):
        # top-bar
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=4)
        ttk.Button(bar, text="⟳ Ανανέωση", command=self._refresh).pack(side="right")
        ttk.Button(bar, text="⚙ Ρυθμίσεις", command=self._open_settings).pack(side="right", padx=4)
        ttk.Label(bar, text="Κατηγορία:").pack(side="left")
        self.filter_var = tk.StringVar(value="all")
        combo = ttk.Combobox(
            bar,
            textvariable=self.filter_var,
            values=["all", "offers", "community", "requests"],
            state="readonly",
            width=14,
        )
        combo.pack(side="left", padx=4)
        combo.bind("<<ComboboxSelected>>", lambda *_: self._populate())

        # list
        cols = ("id", "category", "title", "timestamp", "read")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="w", width=110 if c == "id" else 140)
        self.tree.pack(fill="both", expand=True, pady=2)

        # action buttons
        acts = ttk.Frame(self)
        acts.pack(fill="x", pady=4)
        ttk.Button(acts, text="Λεπτομέρειες", command=self._details).pack(side="left")
        ttk.Button(acts, text="✔ Διαβασμένο", command=self._mark_read).pack(side="left", padx=4)
        ttk.Button(acts, text="🗑 Διαγραφή", command=self._delete).pack(side="left")
        ttk.Button(acts, text="↩ Κεντρικό Μενού", command=self.destroy).pack(side="right")

        self._refresh()

    # ───────── helpers ────────────────────────────────────────────────────────
    def _populate(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        cat = None if self.filter_var.get() == "all" else self.filter_var.get()
        for n in self.service.list(category=cat):
            self.tree.insert(
                "",
                "end",
                iid=n.id,
                values=(
                    n.id,
                    n.category,
                    n.title,
                    n.timestamp.strftime("%d/%m %H:%M"),
                    "Ναι" if n.read else "‒",
                ),
            )

    def _sel(self) -> Optional[int]:
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    # ───────── actions (map to UC steps) ──────────────────────────────────────
    def _refresh(self):
        self.service.refresh()
        self._populate()

    def _mark_read(self):
        nid = self._sel()
        if nid and self.service.mark_read(nid):
            self._populate()

    def _delete(self):
        nid = self._sel()
        if nid and self.service.delete(nid):
            self._populate()

    def _details(self):
        nid = self._sel()
        if not nid:
            return
        n = next(x for x in self.service.list() if x.id == nid)
        messagebox.showinfo(title=n.title, message=n.content)

    def _open_settings(self):
        ns.SettingsWindow(self, self.service)


if __name__ == "__main__":
    NotificationApp(NotificationService()).mainloop()
