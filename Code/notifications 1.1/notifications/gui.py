# notifications/gui.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty

from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog

from .notifications import NotificationService
from .notifications_settings import SettingsWindow

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: "Ειδοποιήσεις"
        left_action_items: [["cog", lambda x: app.open_settings()]]
        right_action_items: [["refresh", lambda x: app.refresh()]]
        md_bg_color: app.theme_cls.primary_color

    BoxLayout:
        size_hint_y: None
        height: dp(48)
        padding: dp(8)
        spacing: dp(8)

        MDLabel:
            text: "Κατηγορία:"
            size_hint_x: None
            width: dp(80)
            valign: "center"

        Spinner:
            id: filter_spinner
            text: "all"
            values: ["all", "offers", "community", "requests"]
            size_hint_x: None
            width: dp(120)
            on_text: app.update_list()

    ScrollView:
        MDList:
            id: md_list

    BoxLayout:
        size_hint_y: None
        height: dp(56)
        spacing: dp(8)
        padding: dp(8)

        MDRaisedButton:
            text: "Λεπτομέρειες"
            on_release: app.show_details()

        MDRaisedButton:
            text: "✔ Διαβασμένο"
            on_release: app.mark_read()

        MDRaisedButton:
            text: "🗑 Διαγραφή"
            on_release: app.delete_notification()

        MDRaisedButton:
            text: "↩ Κεντρικό Μενού"
            on_release: app.stop()
'''

class NotificationApp(MDApp):
    # default to 0 so it's never None
    selected_id = NumericProperty(0)

    def build(self):
        self.service = NotificationService()
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def on_start(self):
        # seed it so the list is never empty
        self.service.refresh(n_fake=1)
        self.update_list()

    def refresh(self):
        self.service.refresh()
        self.update_list()

    def update_list(self):
        md_list = self.root.ids.md_list
        md_list.clear_widgets()

        cat = self.root.ids.filter_spinner.text
        cat = None if cat == "all" else cat

        for n in self.service.list(category=cat):
            base = (
                f"{n.id} | {n.category} | {n.title} | "
                f"{n.timestamp.strftime('%d/%m %H:%M')} | "
                f"{'Ναι' if n.read else '-'}"
            )
            item = OneLineListItem(text=base)
            item.nid = n.id
            # color the selected one
            if n.id == self.selected_id:
                item.theme_text_color = "Custom"
                item.text_color = self.theme_cls.primary_color
            else:
                item.theme_text_color = "Primary"

            item.bind(on_release=self.on_item_release)
            md_list.add_widget(item)

    def on_item_release(self, instance):
        # record which item was tapped, then redraw to highlight
        self.selected_id = instance.nid
        self.update_list()

    def show_details(self):
        if not self.selected_id:
            return
        n = next((x for x in self.service.list() if x.id == self.selected_id), None)
        if n:
            MDDialog(
                title=n.title,
                text=n.content,
                size_hint=(0.8, 0.4),
            ).open()

    def mark_read(self):
        if self.selected_id and self.service.mark_read(self.selected_id):
            self.update_list()

    def delete_notification(self):
        if self.selected_id and self.service.delete(self.selected_id):
            # reset to “none” by using 0
            self.selected_id = 0
            self.update_list()

    def open_settings(self):
        SettingsWindow()

if __name__ == "__main__":
    NotificationApp().run()
