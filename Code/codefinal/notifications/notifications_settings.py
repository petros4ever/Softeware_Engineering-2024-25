"""
Dummy settings window – fulfils bullet
“Μπορεί να μεταβεί στις ρυθμίσεις ειδοποιήσεων…”
"""

import tkinter as tk
from tkinter import ttk
from notifications import NotificationService


class SettingsWindow(tk.Toplevel):
    def __init__(self, master, service: NotificationService):
        super().__init__(master)
        self.service = service
        self.title("Ρυθμίσεις ειδοποιήσεων")
        ttk.Label(self, text="(υπό υλοποίηση…)").pack(padx=30, pady=30)
