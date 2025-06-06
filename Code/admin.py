from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, IRightBodyTouch
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

KV = """
ScreenManager:
    MainScreen:
    AdminScreen:
    UploadScreen:

<MainScreen>:
    name: "main"

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Admin Dashboard"
            right_action_items: [["account", lambda x: app.show_profile()]]

        MDTextField:
            hint_text: "Search books"
            icon_right: "magnify"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}

        ScrollView:
            MDBoxLayout:
                id: book_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: "10dp"
                spacing: "10dp"

        MDRaisedButton:
            text: "Admin Panel"
            pos_hint: {"center_x": 0.5}
            on_release: app.switch_to_admin_panel()

<AdminScreen>:
    name: "admin"

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Admin Panel"
            left_action_items: [["arrow-left", lambda x: app.switch_to_main_screen()]]

        MDBoxLayout:
            orientation: 'vertical'
            spacing: "20dp"
            padding: "20dp"

            MDRaisedButton:
                text: "Ανέβασμα Βιβλίων"
                pos_hint: {"center_x": 0.5}
                on_release: app.switch_to_upload_screen()

            MDRaisedButton:
                text: "Έκπτωση Κατηγορίας Βιβλίου"
                pos_hint: {"center_x": 0.5}
                on_release: app.discount_category()
                
            MDTextField:
                id: category_name
                hint_text: "Κατηγορία για Έκπτωση"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}

            MDTextField:
                id: discount_percentage
                hint_text: "Ποσοστό Έκπτωσης"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                input_filter: "float"

            MDRaisedButton:
                text: "Διαγραφή Κακόβουλου Σχολίου"
                pos_hint: {"center_x": 0.5}
                on_release: app.delete_comment()

<UploadScreen>:
    name: "upload"

    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "10dp"

        MDTopAppBar:
            title: "Upload Book"
            left_action_items: [["arrow-left", lambda x: app.switch_to_admin_panel()]]

        MDTextField:
            id: book_name
            hint_text: "Όνομα Βιβλίου"

        MDTextField:
            id: author_name
            hint_text: "Συγγραφέας"

        MDTextField:
            id: book_price
            hint_text: "Τιμή Βιβλίου"
            input_filter: "float"

        MDTextField:
            id: book_category
            hint_text: "Κατηγορία"

        MDRaisedButton:
            text: "Αποθήκευση"
            pos_hint: {"center_x": 0.5}
            on_release: app.save_book()
"""


class Book:
    def __init__(self, name, author, price):
        self.name = name
        self.author = author
        self.price = price


class MainScreen(MDScreen):
    pass


class AdminScreen(MDScreen):
    pass


class UploadScreen(MDScreen):
    pass


class AdminApp(MDApp):
    def build(self):
        self.books = {
            "Fiction": [Book("Book 1", "Author A", "10.99"), Book("Book 2", "Author B", "12.50")],
            "Technology": [Book("AI Revolution", "John Smith", "25.00"),
                           Book("Cyber Security 101", "Alice Brown", "30.00")]
        }
        return Builder.load_string(KV)

    def on_start(self):
        self.update_book_list()

    def update_book_list(self):
        book_list = self.root.get_screen('main').ids.book_list
        book_list.clear_widgets()

        for category, books in self.books.items():
            panel_content = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp", spacing="10dp")
            panel_content.add_widget(Label(text="", size_hint_y=None, height=10))  # Add spacing
            for book in books:
                book_item = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding="5dp")
                book_item.add_widget(OneLineListItem(text=f"{book.name} - {book.author} ({book.price}$)"))
                delete_btn = MDIconButton(icon="delete",
                                          on_release=lambda x, c=category, b=book: self.delete_book(c, b))
                book_item.add_widget(delete_btn)
                panel_content.add_widget(book_item)
            book_list.add_widget(
                MDExpansionPanel(
                    content=panel_content,
                    panel_cls=MDExpansionPanelOneLine(text=category)
                )
            )

    def save_book(self):
        name = self.root.get_screen('upload').ids.book_name.text
        author = self.root.get_screen('upload').ids.author_name.text
        price = self.root.get_screen('upload').ids.book_price.text
        category = self.root.get_screen('upload').ids.book_category.text

        if name and author and price and category:
            if category not in self.books:
                self.books[category] = []
            self.books[category].append(Book(name, author, price))
            self.update_book_list()
            self.switch_to_admin_panel()
        else:
            print("Please fill all fields")

    def delete_book(self, category, book):
        if category in self.books and book in self.books[category]:
            self.books[category].remove(book)
            if not self.books[category]:
                del self.books[category]
            self.update_book_list()

    def switch_to_admin_panel(self):
        self.root.current = "admin"

    def switch_to_main_screen(self):
        self.root.current = "main"

    def switch_to_upload_screen(self):
        self.root.current = "upload"

    def discount_category(self):
        # Ζήτα από τον χρήστη την κατηγορία και την έκπτωση
        category = self.root.get_screen('admin').ids.category_name.text  # Παράδειγμα, αν θες το input από το UI
        discount_percentage = float(
            self.root.get_screen('admin').ids.discount_percentage.text)  # Αν το πάρεις από το UI

        if category in self.books:
            for book in self.books[category]:
                book.price = str(round(float(book.price) * (1 - discount_percentage / 100), 2))
            self.update_book_list()
        else:
            print("Η κατηγορία δεν βρέθηκε")


AdminApp().run()
