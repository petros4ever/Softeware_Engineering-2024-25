#Use Case Book Seaching

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu

KV = '''
ScreenManager:
    MainScreen:
    SearchResultsScreen:
    BookDetailScreen:

<MainScreen>:
    name: "main"
    last_search: ""

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "E-Book Store"
            elevation: 10

        MDTextField:
            id: search_field
            hint_text: "Search for books, authors, keywords..."
            size_hint_x: 0.95
            pos_hint: {"center_x": 0.5}
            on_text_validate: root.search_books(search_field.text)
            on_focus: root.show_last_search()

        MDBoxLayout:
            id: last_search_box
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: [20, 10]

            MDLabel:
                id: last_search_label
                text: ""
                theme_text_color: "Hint"
                halign: "left"

            MDRectangleFlatButton:
                id: last_search_button
                text: ""
                on_release: root.search_books(self.text)
                opacity: 0
                disabled: True

        MDLabel:
            text: "Categories"
            halign: "center"
            font_style: "H6"
            padding_y: 10

        ScrollView:
            MDGridLayout:
                cols: 2
                adaptive_height: True
                padding: 10
                spacing: 10

                MDRaisedButton:
                    text: "Fiction"
                    on_release: Snackbar.show(text="Category: Fiction")

                MDRaisedButton:
                    text: "Sci-Fi"
                    on_release: Snackbar.show(text="Category: Sci-Fi")

                MDRaisedButton:
                    text: "Romance"
                    on_release: Snackbar.show(text="Category: Romance")

                MDRaisedButton:
                    text: "Thriller"
                    on_release: Snackbar.show(text="Category: Thriller")


<SearchResultsScreen>:
    name: "results"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: toolbar
            title: "Search Results"
            elevation: 10
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["filter", lambda x: root.open_filter()]]

        ScrollView:
            MDList:
                id: results_list


<BookDetailScreen>:
    name: "book_detail"

    MDBoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10

        MDTopAppBar:
            title: "Book Details"
            left_action_items: [["arrow-left", lambda x: app.go_back_to_results()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: 20
                spacing: 20
                adaptive_height: True

                MDLabel:
                    id: book_title
                    text: ""
                    font_style: "H5"
                    halign: "center"

                MDLabel:
                    id: book_author
                    text: ""
                    font_style: "Subtitle1"
                    halign: "center"

                MDSeparator:

                MDLabel:
                    text: "Summary"
                    font_style: "Subtitle2"
                    bold: True

                MDLabel:
                    id: book_summary
                    text: ""
                    theme_text_color: "Secondary"

                MDLabel:
                    text: "Book Info"
                    font_style: "Subtitle2"
                    bold: True

                MDLabel:
                    id: book_info
                    text: ""

                MDLabel:
                    text: "Author Info"
                    font_style: "Subtitle2"
                    bold: True

                MDLabel:
                    id: author_info
                    text: ""

                MDLabel:
                    text: "Rating"
                    font_style: "Subtitle2"
                    bold: True

                MDLabel:
                    id: book_rating
                    text: ""
'''


# Dummy book data
BOOKS = [
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "summary": "A novel set in the Jazz Age, telling the story of Jay Gatsby’s pursuit of Daisy Buchanan.",
        "info": "Genre: Fiction\nPages: 180\nPublished: 1925",
        "author_info": "Fitzgerald was an American novelist known for depicting the Roaring Twenties.",
        "rating": "★★★★☆"
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "summary": "A science fiction epic about politics, religion, and ecology on the desert planet Arrakis.",
        "info": "Genre: Sci-Fi\nPages: 412\nPublished: 1965",
        "author_info": "Frank Herbert was an American author best known for the Dune series.",
        "rating": "★★★★★"
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "summary": "A romantic novel about manners, marriage, and morality in 19th-century England.",
        "info": "Genre: Romance\nPages: 279\nPublished: 1813",
        "author_info": "Jane Austen was an English novelist known for her social commentary.",
        "rating": "★★★★★"
    },
    {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "summary": "A psychological thriller about a woman who stops speaking after committing a violent crime.",
        "info": "Genre: Thriller\nPages: 336\nPublished: 2019",
        "author_info": "Michaelides is a British-Cypriot author and screenwriter.",
        "rating": "★★★★☆"
    },
]


class MainScreen(Screen):
    last_search = ""

    def search_books(self, query):
        if not query.strip():
            Snackbar.show(text="Please enter a search term.")
            return

        self.last_search = query
        self.ids.last_search_label.text = "Last search:"
        self.ids.last_search_button.text = query
        self.ids.last_search_button.opacity = 1
        self.ids.last_search_button.disabled = False

        results = [
            book for book in BOOKS
            if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()
        ]
        self.manager.get_screen("results").set_results(results)
        self.manager.current = "results"

    def show_last_search(self):
        if self.last_search:
            self.ids.last_search_label.text = "Last search:"
            self.ids.last_search_button.text = self.last_search
            self.ids.last_search_button.opacity = 1
            self.ids.last_search_button.disabled = False
        else:
            self.ids.last_search_label.text = ""
            self.ids.last_search_button.text = ""
            self.ids.last_search_button.opacity = 0
            self.ids.last_search_button.disabled = True


class SearchResultsScreen(Screen):
    def on_pre_enter(self):
        if not hasattr(self, 'menu'):
            menu_items = [
                {"text": "Sort by Title", "on_release": lambda x="title": self.apply_sort(x)},
                {"text": "Sort by Author", "on_release": lambda x="author": self.apply_sort(x)},
            ]
            self.menu = MDDropdownMenu(
                caller=self.ids.toolbar,
                items=menu_items,
                width_mult=4,
                max_height=dp(100)
            )

    def set_results(self, books):
        self.books = books
        self.display_results()

    def display_results(self):
        self.ids.results_list.clear_widgets()
        if not self.books:
            self.ids.results_list.add_widget(OneLineListItem(text="No results found."))
        else:
            for book in self.books:
                item = OneLineListItem(
                    text=f"{book['title']} by {book['author']}",
                    on_release=lambda instance, b=book: self.open_book_detail(b)
                )
                self.ids.results_list.add_widget(item)

    def open_filter(self):
        self.menu.open()

    def apply_sort(self, key):
        self.books.sort(key=lambda x: x[key].lower())
        self.display_results()
        self.menu.dismiss()

    def open_book_detail(self, book):
        detail_screen = self.manager.get_screen("book_detail")
        detail_screen.set_book_data(book)
        self.manager.current = "book_detail"


class BookDetailScreen(Screen):
    def set_book_data(self, book):
        self.ids.book_title.text = book["title"]
        self.ids.book_author.text = f"by {book['author']}"
        self.ids.book_summary.text = book["summary"]
        self.ids.book_info.text = book["info"]
        self.ids.author_info.text = book["author_info"]
        self.ids.book_rating.text = book["rating"]


class EBookApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def go_back(self):
        self.root.current = "main"

    def go_back_to_results(self):
        self.root.current = "results"


if __name__ == "__main__":
    EBookApp().run()
