"""
Comment-moderation demo  –  Kivy 2.3.1  +  KivyMD 1.2.0
-------------------------------------------------------
• User adds comments.
• User flags a comment → dialog with four reason buttons
  (Spam / Offensive / Harassment / Other).
• Toast: “Admin notified – reason”.
• Admin panel shows reported items; trash can deletes.
• All data lives in RAM (restart clears).

Crash-proof: no DropdownMenu, no Snackbar, only MDDialog + toast().
"""

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton

# ──────────────────── KV LAYOUT ────────────────────
KV = """
ScreenManager:
    User:
    Admin:

<User@MDScreen>:
    name: "user"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Comments"
            elevation: 10
            right_action_items: [["shield", lambda x: app.go_admin()]]

        MDTextField:
            id: in_comment
            hint_text: "Write a comment…"
            multiline: False
            size_hint_y: None
            height: dp(48)
            pos_hint: {"center_x": .5}
            on_text_validate: app.add_comment()

        MDRaisedButton:
            text: "Add Comment"
            size_hint_x: None
            width: dp(140)
            pos_hint: {"center_x": .5}
            on_release: app.add_comment()

        ScrollView:
            MDList:
                id: list_comments


<Admin@MDScreen>:
    name: "admin"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Admin Panel"
            elevation: 10
            left_action_items: [["arrow-left", lambda x: app.go_user()]]

        ScrollView:
            MDList:
                id: list_reports
"""

# ──────────────────── DATA ─────────────────────────
DATA = {"next_id": 1, "comments": []}
REASONS = ["Spam", "Offensive", "Harassment", "Other"]

# ─────────────────── LIST ROWS ─────────────────────
class CommentRow(OneLineAvatarIconListItem):
    comment_id = NumericProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        flag = IconRightWidget(icon="flag")
        flag.bind(on_release=self.open_reason_dialog)
        self.add_widget(flag)

    def open_reason_dialog(self, *_):
        # Build dialog once per click; keep ref so we can close it.
        buttons = [
            MDFlatButton(
                text=r,
                on_release=lambda btn, r=r: self.report(r)
            )
            for r in REASONS
        ]
        self._dlg = MDDialog(title="Report reason", buttons=buttons)
        self._dlg.open()

    def report(self, reason):
        self._dlg.dismiss()

        # update data
        for c in DATA["comments"]:
            if c["id"] == self.comment_id:
                c.update(reported=True, reason=reason)
                break

        toast(f"Admin notified – {reason}")
        # refresh UI after dialog animation frame
        Clock.schedule_once(lambda dt: MDApp.get_running_app().refresh_all(), 0)


class ReportRow(OneLineAvatarIconListItem):
    comment_id = NumericProperty()
    reason = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        trash = IconRightWidget(icon="delete")
        trash.bind(on_release=self.confirm_delete)
        self.add_widget(trash)

    def confirm_delete(self, *_):
        def really_delete(*_):
            DATA["comments"][:] = [
                c for c in DATA["comments"] if c["id"] != self.comment_id
            ]
            dlg.dismiss()
            toast("Comment deleted.")
            MDApp.get_running_app().refresh_all()

        dlg = MDDialog(
            title="Delete comment?",
            text=f"{self.text}\n\nReason: {self.reason}",
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda *_: dlg.dismiss()),
                MDRaisedButton(
                    text="Delete",
                    md_bg_color=MDApp.get_running_app().theme_cls.error_color,
                    on_release=really_delete,
                ),
            ],
        )
        dlg.open()


# ──────────────────── MAIN APP ─────────────────────
class App(MDApp):
    def build(self):
        Window.minimum_width, Window.minimum_height = (420, 720)
        return Builder.load_string(KV)

    # navigation
    def go_admin(self, *_): self.root.current = "admin"
    def go_user(self, *_):  self.root.current = "user"

    # add comment
    def add_comment(self, *_):
        field = self.root.get_screen("user").ids.in_comment
        txt = field.text.strip()
        if not txt:
            return
        DATA["comments"].append(
            {"id": DATA["next_id"], "text": txt, "reported": False, "reason": ""}
        )
        DATA["next_id"] += 1
        field.text = ""
        self.refresh_all()

    # refreshers
    def refresh_all(self):
        self._refresh_user()
        self._refresh_admin()

    def _refresh_user(self):
        lst = self.root.get_screen("user").ids.list_comments
        lst.clear_widgets()
        for c in DATA["comments"]:
            row = CommentRow(text=c["text"], comment_id=c["id"])
            if c["reported"]:
                row.text = f"[color=#FF5722]{c['text']}[/color]"; row.markup = True
            lst.add_widget(row)

    def _refresh_admin(self):
        lst = self.root.get_screen("admin").ids.list_reports
        lst.clear_widgets()
        for c in DATA["comments"]:
            if c["reported"]:
                lst.add_widget(
                    ReportRow(text=c["text"], comment_id=c["id"], reason=c["reason"])
                )


if __name__ == "__main__":
    App().run()
