from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
import json
import os

KV = '''
ScreenManager:
    MainScreen:
    LibraryScreen:
    ReadingScreen:
    NotesScreen:

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.94, 0.89, 0.84, 1
        MDTopAppBar:
            title: 'P.R.I.M.A.L.'
            md_bg_color: 0.0, 0.36, 0.36, 1
        MDRaisedButton:
            text: 'Πήγαινε στη Βιβλιοθήκη'
            on_release: app.change_screen('library')

<LibraryScreen>:
    name: 'library'
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.9
            md_bg_color: 0.94, 0.89, 0.84, 1

            MDTopAppBar:
                title: 'Library'
                md_bg_color: 0.0, 0.36, 0.36, 1
                left_action_items: [['arrow-left', lambda x: app.change_screen('main')]]

            MDTextField:
                id: search_field
                hint_text: 'Search'
                on_text: app.search_books(self.text)
                size_hint_y: None
                height: dp(48)
                mode: 'rectangle'

            ScrollView:
                MDGridLayout:
                    id: book_grid
                    cols: 3
                    adaptive_height: True
                    padding: dp(8)
                    spacing: dp(8)

        MDBottomNavigation:
            size_hint_y: 0.1
            MDBottomNavigationItem:
                name: 'library_nav'
                text: 'Library'
                icon: 'book'
            MDBottomNavigationItem:
                name: 'notes_nav'
                text: 'Notes'
                icon: 'note-text'
                on_tab_press: app.change_screen('notes')

<ReadingScreen>:
    name: 'reading'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.94, 0.89, 0.84, 1
        MDTopAppBar:
            title: root.book_title
            md_bg_color: 0.0, 0.36, 0.36, 1
            left_action_items: [['arrow-left', lambda x: app.save_bookmark_and_back()]]
        MDLabel:
            id: page_label
            text: ''
            halign: 'center'
        MDRaisedButton:
            text: 'Επόμενη σελίδα'
            on_release: app.next_page()

<NotesScreen>:
    name: 'notes'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.94, 0.89, 0.84, 1
        MDTopAppBar:
            title: 'Notes'
            md_bg_color: 0.0, 0.36, 0.36, 1
            left_action_items: [['arrow-left', lambda x: app.change_screen('library')]]
        MDTextField:
            id: note_input
            hint_text: 'Γράψε σημείωση για το βιβλίο'
            multiline: True
            size_hint_y: 0.8
        MDRaisedButton:
            text: 'Αποθήκευση'
            on_release: app.save_note()
'''

class MainScreen(Screen):
    pass

class LibraryScreen(Screen):
    pass

class ReadingScreen(Screen):
    book_title = StringProperty('')

class NotesScreen(Screen):
    pass

class EBookApp(MDApp):
    def build(self):
        self.title = "eBookApp"
        self.theme_cls.primary_palette = "Teal"
        self.load_books()
        self.load_bookmarks()
        self.load_notes()
        self.current_page = 0
        return Builder.load_string(KV)

    def load_books(self):
        if os.path.exists("books.json"):
            with open("books.json", "r") as f:
                self.books = json.load(f)
        else:
            self.books = [
                {"title": "Clean Code", "cover": "covers/clean_code.jpg"},
                {"title": "Computer Networks", "cover": "covers/networks.jpg"},
                {"title": "Introduction to Algorithms", "cover": "covers/algorithms.jpg"},
                {"title": "Operating System Concepts", "cover": "covers/os.jpg"},
                {"title": "Design Patterns", "cover": "covers/design_patterns.jpg"},
                {"title": "Database System Concepts", "cover": "covers/db.jpg"},
                {"title": "Artificial Intelligence", "cover": "covers/ai.jpg"}
            ]

    def load_bookmarks(self):
        if os.path.exists("bookmark.json"):
            with open("bookmark.json", "r") as f:
                self.bookmarks = json.load(f)
        else:
            self.bookmarks = {}

    def save_bookmarks(self):
        with open("bookmark.json", "w") as f:
            json.dump(self.bookmarks, f)

    def load_notes(self):
        if os.path.exists("notes.json"):
            with open("notes.json", "r") as f:
                self.notes = json.load(f)
        else:
            self.notes = {}

    def save_notes(self):
        with open("notes.json", "w") as f:
            json.dump(self.notes, f)

    def on_start(self):
        self.display_books(self.books)

    def display_books(self, book_list):
        grid = self.root.get_screen('library').ids.book_grid
        grid.clear_widgets()
        for book in book_list:
            card = MDCard(orientation='vertical', size_hint_y=None, height='220dp', ripple_behavior=True)
            image = AsyncImage(source=book['cover'], size_hint_y=0.8)
            label = MDLabel(text=book['title'], halign='center', size_hint_y=0.2)
            card.add_widget(image)
            card.add_widget(label)
            card.bind(on_release=lambda instance, b=book: self.open_book(b))
            grid.add_widget(card)

    def search_books(self, text):
        filtered = [b for b in self.books if text.lower() in b['title'].lower()]
        self.display_books(filtered)

    def open_book(self, book):
        self.current_book = book['title']
        self.current_page = self.bookmarks.get(self.current_book, 1)
        screen = self.root.get_screen('reading')
        screen.book_title = self.current_book
        self.update_page_label()
        self.change_screen('reading')

    def next_page(self):
        self.current_page += 1
        self.update_page_label()

    def update_page_label(self):
        page_label = self.root.get_screen('reading').ids.page_label
        page_label.text = f"{self.current_book} - Σελίδα {self.current_page}"

    def save_bookmark_and_back(self):
        self.bookmarks[self.current_book] = self.current_page
        self.save_bookmarks()
        self.change_screen('library')

    def save_note(self):
        note = self.root.get_screen('notes').ids.note_input.text
        if self.current_book:
            self.notes[self.current_book] = note
            self.save_notes()

    def change_screen(self, screen_name):
        self.root.current = screen_name

if __name__ == '__main__':
    EBookApp().run()
