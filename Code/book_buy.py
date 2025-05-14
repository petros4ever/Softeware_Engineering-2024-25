from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.list import OneLineIconListItem, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView

# --- Domain Models ---
class Book:
    def __init__(self, name, author, price, pages, rating, category, description):
        self.name = name
        self.author = author
        self.price = price
        self.pages = pages
        self.rating = rating
        self.category = category
        self.description = description

# Sample book data
BOOKS = [
    Book("Software Engineering", "Ian Sommerville", 24.99, 864, 4.3, "Software Engineering",
         "A widely respected textbook covering key software development principles, methodologies, and practices."),
    Book("Data Structures", "Mark Weiss", 18.75, 500, 4.2, "Software Engineering",
         "Comprehensive introduction to data structures with in-depth examples."),
    Book("Clean Code", "Robert Martin", 21.00, 464, 4.6, "Software Engineering",
         "Guide to writing clean, maintainable, and efficient code."),
    Book("Gray's Anatomy", "Henry Gray", 30.50, 1500, 4.7, "Medicine",
         "Definitive reference for human anatomy used by medical professionals worldwide."),
    Book("Pathology Essentials", "Robbins", 27.40, 980, 4.5, "Medicine",
         "Fundamentals of pathology and disease processes with rich visuals."),
]

# --- Screens ---
class HomeScreen(Screen):
    pass

class BookDetailScreen(Screen):
    def set_book(self, book: Book):
        self.ids.title.text = book.name
        self.ids.author.text = f"by {book.author}"
        self.ids.rating.text = f"Rating: {book.rating} ★ ({book.pages} pages)"
        self.ids.description.clear_widgets()
        self.ids.description.add_widget(MDLabel(text=book.description, theme_text_color="Secondary", size_hint_y=None, height=self.ids.description.height, text_color="#333333"))
        self.ids.price_button.text = f"Add to Cart (€{book.price:.2f})"
        self.book = book

    def add_to_cart(self):
        app = MDApp.get_running_app()
        app.cart.append(self.book)
        app.update_cart()
        app.show_dialog(f"Added {self.book.name} to cart.")

    def go_back(self):
        MDApp.get_running_app().screen.current = "home"

# --- Main App ---
KV = '''
ScreenManager:
    HomeScreen:
    BookDetailScreen:

<HomeScreen>:
    name: "home"
    md_bg_color: "#F5F0E1"
    MDBottomNavigation:
        panel_color: "#F5F0E1"

        MDBottomNavigationItem:
            name: 'home'
            text: 'Home'
            icon: 'home'

            MDBoxLayout:
                orientation: 'vertical'
                md_bg_color: "#F5F0E1"

                MDTextField:
                    id: search_field
                    hint_text: "Search"
                    size_hint_y: None
                    height: "40dp"
                    pos_hint: {"center_x": 0.5}
                    on_text_validate: app.search_books(self.text)
                    mode: "rectangle"
                    color_mode: "custom"
                    line_color_normal: "#004d40"
                    text_color: "#333333"

                ScrollView:
                    MDBoxLayout:
                        id: book_list
                        orientation: 'vertical'
                        padding: 10
                        spacing: 10
                        size_hint_y: None
                        height: self.minimum_height

        MDBottomNavigationItem:
            name: 'cart'
            text: 'Cart'
            icon: 'cart'

            MDBoxLayout:
                orientation: 'vertical'
                padding: 20
                md_bg_color: "#F5F0E1"

                MDLabel:
                    text: 'Cart Items'
                    halign: 'center'
                    theme_text_color: 'Primary'
                    text_color: "#333333"

                ScrollView:
                    MDBoxLayout:
                        id: cart_list
                        orientation: 'vertical'
                        padding: 10
                        spacing: 10
                        size_hint_y: None
                        height: self.minimum_height

                MDRaisedButton:
                    text: 'Checkout'
                    pos_hint: {"center_x": 0.5}
                    md_bg_color: "#004d40"
                    on_release: app.checkout()

<BookDetailScreen>:
    name: "details"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        md_bg_color: "#F5F0E1"

        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_x": 0.0}
            on_release: root.go_back()

        MDLabel:
            id: title
            text: "Book Title"
            font_style: "H5"
            halign: "center"
            theme_text_color: "Primary"
            text_color: "#333333"

        MDLabel:
            id: author
            text: "Author"
            halign: "center"
            theme_text_color: "Secondary"
            text_color: "#333333"

        MDLabel:
            id: rating
            text: "Rating and pages"
            halign: "center"
            theme_text_color: "Secondary"
            text_color: "#333333"

        ScrollView:
            id: description
            size_hint_y: 0.4
            MDBoxLayout:
                orientation: "vertical"
                padding: 10
                size_hint_y: None
                height: self.minimum_height

        MDRaisedButton:
            id: price_button
            text: "Add to Cart"
            md_bg_color: "#004d40"
            on_release: root.add_to_cart()
'''

class EBookApp(MDApp):
    dialog = None
    cart = []

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.screen = Builder.load_string(KV)
        self.populate_home()
        return self.screen

    def populate_home(self):
        container = self.screen.get_screen("home").ids.book_list
        container.clear_widgets()
        categories = set(book.category for book in BOOKS)
        for category in categories:
            container.add_widget(MDLabel(text=category, bold=True, theme_text_color="Primary", text_color="#333333"))
            for book in [b for b in BOOKS if b.category == category]:
                item = OneLineAvatarIconListItem(
                    text=f"{book.name} - €{book.price:.2f}",
                    on_release=lambda x, b=book: self.show_book_details(b)
                )
                icon = IconLeftWidget(icon="book-open-page-variant")
                item.add_widget(icon)
                container.add_widget(item)

    def search_books(self, query):
        results = [b for b in BOOKS if query.lower() in b.name.lower() or query.lower() in b.author.lower()]
        container = self.screen.get_screen("home").ids.book_list
        container.clear_widgets()
        for book in results:
            item = OneLineAvatarIconListItem(
                text=f"{book.name} - €{book.price:.2f}",
                on_release=lambda x, b=book: self.show_book_details(b)
            )
            icon = IconLeftWidget(icon="book-open-page-variant")
            item.add_widget(icon)
            container.add_widget(item)

    def show_book_details(self, book):
        detail_screen = self.screen.get_screen("details")
        detail_screen.set_book(book)
        self.screen.current = "details"

    def update_cart(self):
        cart_container = self.screen.get_screen("home").ids.cart_list
        cart_container.clear_widgets()
        for book in self.cart:
            cart_container.add_widget(MDLabel(text=f"{book.name} - €{book.price:.2f}", text_color="#333333"))

    def checkout(self):
        total = sum(book.price for book in self.cart)
        self.cart.clear()
        self.update_cart()
        self.show_dialog(f"Purchase completed! Total paid: €{total:.2f}")

    def show_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(title="Notification", text=message,
                               buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()

EBookApp().run()