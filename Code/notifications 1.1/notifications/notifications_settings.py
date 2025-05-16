# Simple settings dialog placeholder.

from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.label import MDLabel

KV_SETTINGS = """
<SettingsContent>:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(20)
    MDLabel:
        text: "Επιλογές Ειδοποιήσεων (υπό κατασκευή)"
        halign: "center"
"""

class SettingsContent(MDBoxLayout):
    pass

Builder.load_string(KV_SETTINGS)

class SettingsWindow:
    def __init__(self):
        self.dialog = MDDialog(
            title="Ρυθμίσεις Ειδοποιήσεων",
            type="custom",
            content_cls=SettingsContent(),
            size_hint=(0.8, 0.5),
        )
        self.dialog.open()
