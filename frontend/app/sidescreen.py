from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, OneLineIconListItem, IconRightWidget
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout, MDNavigationDrawerMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.toolbar import MDTopAppBar

KV = """
MDNavigationLayout:
    ScreenManager:
        Screen:
            MDTopAppBar:
                title: ""
                elevation: 0
                pos_hint: {"top": 1}
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 20, 20, 0)
        md_bg_color: 72/255, 99/255, 106/255, 1

        MDBoxLayout:
            orientation: "vertical"
            padding: "10dp"
            spacing: "10dp"

            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: "150dp"
                padding: "10dp"
                spacing: "5dp"

                MDIconButton:
                    icon: "account-circle"
                    user_font_size: "48sp"
                    theme_text_color: "Custom"
                    text_color: 201/255, 192/255, 177/255, 1
                    pos_hint: {"center_x": 0.5}

                MDLabel:
                    text: "User1"
                    theme_text_color: "Custom"
                    text_color: 201/255, 192/255, 177/255, 1
                    halign: "center"
                MDLabel:
                    text: "user1@gmail.com"
                    theme_text_color: "Custom"
                    text_color: 201/255, 192/255, 177/255, 1
                    halign: "center"
                    font_style: "Caption"

            ScrollView:
                MDList:
                    OneLineIconListItem:
                        text: "Profile"
                        theme_text_color: "Custom"
                        text_color: 201/255, 192/255, 177/255, 1
                        IconLeftWidget:
                            icon: "account"
                            theme_text_color: "Custom"
                            text_color: 201/255, 192/255, 177/255, 1

                    OneLineIconListItem:
                        text: "Notebook"
                        theme_text_color: "Custom"
                        text_color: 201/255, 192/255, 177/255, 1
                        IconLeftWidget:
                            icon: "notebook"
                            theme_text_color: "Custom"
                            text_color: 201/255, 192/255, 177/255, 1

                    OneLineIconListItem:
                        text: "Wallet"
                        theme_text_color: "Custom"
                        text_color: 201/255, 192/255, 177/255, 1
                        IconLeftWidget:
                            icon: "wallet"
                            theme_text_color: "Custom"
                            text_color: 201/255, 192/255, 177/255, 1

                    OneLineIconListItem:
                        text: "Support"
                        theme_text_color: "Custom"
                        text_color: 201/255, 192/255, 177/255, 1
                        IconLeftWidget:
                            icon: "help-circle"
                            theme_text_color: "Custom"
                            text_color: 201/255, 192/255, 177/255, 1
                    OneLineIconListItem:
                        text: "Settings"
                        theme_text_color: "Custom"
                        text_color: 201/255, 192/255, 177/255, 1
                        IconLeftWidget:
                            icon: "cog"
                            theme_text_color: "Custom"
                            text_color: 201/255, 192/255, 177/255, 1


            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                padding: "10dp"

                OneLineIconListItem:
                    text: "Log out"
                    theme_text_color: "Custom"
                    text_color: 201/255, 192/255, 177/255, 1
                    IconLeftWidget:
                        icon: "logout"
                        theme_text_color: "Custom"
                        text_color: 201/255, 192/255, 177/255, 1
"""


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


if __name__ == "__main__":
    MainApp().run()
