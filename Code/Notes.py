from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from datetime import datetime
import re

Window.size = (360, 640)  # Simulate a mobile device

class CircularButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Transparent to draw custom shape
        self.color = (1, 1, 1, 1)
        self.font_size = 24

        with self.canvas.before:
            Color(0.2, 0.6, 0.86, 1)  # Blue
            self.circle = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

# Custom class to combine BoxLayout and ButtonBehavior
class ClickableBox(ButtonBehavior, BoxLayout):
    def __init__(self, parent, note_data, **kwargs):
        super().__init__(**kwargs)
        self.parent_app = parent  # Store reference to NotesApp or the correct parent
        self.note_data = note_data  # Store note data

        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 80
        self.padding = [10, 10]
        self.spacing = 5

    def on_press(self):
        # Call show_edit_popup on the parent (NotesApp or appropriate class)
        self.parent_app.show_edit_popup(self.note_data)

class TransparentCloser(ButtonBehavior, Widget):
    def __init__(self, popup_ref, **kwargs):
        super().__init__(**kwargs)
        self.popup_ref = popup_ref
        self.size_hint = (None, 1)
        self.width = Window.width * 0.2  # 20% width
        self.background_color = (0, 0, 0, 0)  # Fully transparent
        self.pos = (0, 0)  # Positioned at the left 20%
        self.bind(size=self.update_size)

    def on_press(self):
        self.popup_ref.dismiss()

    def update_size(self, *args):
        self.width = Window.width * 0.2
        self.pos = (0, 0)  # Keep it at the left side of the screen


class NoteItem(ButtonBehavior, BoxLayout):
    pass

class NotesPopup(ModalView):
    def __init__(self, notes, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.background_color = (0, 0, 0, 0)
        self.size_hint = (1, 1)

        # Store the passed notes list
        self.notes = notes
        self.sort_order = 'chronological'  # Default sort order
        self.setup_ui()

    def setup_ui(self):
        root = FloatLayout()

        # Add transparent closer to the left 20% of the screen
        closer = TransparentCloser(self)
        root.add_widget(closer)

        # Drawer area (right 80%)
        self.drawer = BoxLayout(orientation='vertical',
                                size_hint=(None, 1),
                                width=Window.width * 0.8,
                                pos=(Window.width * 0.2, 0),
                                padding=20,
                                spacing=10)

        with self.drawer.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.drawer.pos, size=self.drawer.size)

        self.drawer.bind(pos=self.update_rect, size=self.update_rect)


        # Header using FloatLayout
        header = FloatLayout(size_hint_y=None, height=50)

        with header.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.header_rect = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self.update_header_rect, size=self.update_header_rect)

        # Title label centered in the header
        title_label = Label(text="Notes", font_size=20, color=(0, 0, 0, 1), size_hint=(None, None))
        title_label.size = title_label.texture_size  # Ensure the size of the label is correct
        title_label.pos_hint = {"center_x": 0.5, "center_y": 0.5}  # Center the title horizontally and vertically
        header.add_widget(title_label)
       
        # Sort button with adjusted size
        sort_button = Button(
            text="[b]⇅[/b]",
            font_name='DejaVuSans.ttf',
            markup=True,
            size_hint=(None, None),
            size=(30, 50),  # Adjust height to match the header
            background_normal="",
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size=14,
            bold=True,
            pos_hint={"right": 1, "top": 1},  # Align the button to the top right of the header
        )
        sort_button.bind(on_press=self.toggle_sort_order)
        header.add_widget(sort_button)

        self.drawer.add_widget(header)


        # Scrollable notes list
        self.notes_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=[0, 10])
        self.notes_container.bind(minimum_height=self.notes_container.setter('height'))

        # Refresh notes to show them in reverse order (most recent at top)
        self.refresh_notes()

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.notes_container)
        self.drawer.add_widget(scroll)

        root.add_widget(self.drawer)

        # Add "New Note" button at bottom right
        new_note_btn = Button(
            text="+",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'right': 0.98, 'y': 0.02},
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            font_size=32
        )
        new_note_btn.bind(on_press=self.create_new_note)
        root.add_widget(new_note_btn)

        self.add_widget(root)
        Window.bind(on_resize=self.reposition)

    def update_rect(self, *args):
        self.rect.pos = self.drawer.pos
        self.rect.size = self.drawer.size

    def update_header_rect(self, *args):
        self.header_rect.pos = self.drawer.children[-1].pos
        self.header_rect.size = self.drawer.children[-1].size

    def reposition(self, instance, width, height):
        self.drawer.pos = (width * 0.2, 0)
        self.drawer.width = width * 0.8

    def create_note_widget(self, note_data):
        # Create a note widget with a delete button (as before)
        box = ClickableBox(self, note_data)

        # Add background color to the note
        with box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            rect = Rectangle(pos=box.pos, size=box.size)
            box.bind(pos=lambda inst, val: setattr(rect, 'pos', val),
                     size=lambda inst, val: setattr(rect, 'size', val))

        # Add the title and date to the note
        title_label = Label(text=note_data["title"], color=(0, 0, 0, 1), font_size=16, size_hint_y=None, height=30)
        date_label = Label(text=note_data["date"].strftime('%Y-%m-%d %H:%M'), color=(0.3, 0.3, 0.3, 1), font_size=12, size_hint_y=None, height=20)

        box.add_widget(title_label)
        box.add_widget(date_label)

        return box


    def show_edit_popup(self, note_data):
        # Create a popup to edit the note
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add the title input (smaller)
        title_input = TextInput(text=note_data["title"], multiline=False, size_hint_y=None, height=40)
        
        # Title label with proper alignment and size hint
        title_label = Label(text="Title:", size_hint_y=None, height=30, halign='left', valign='middle')

        # Add the title label and input vertically stacked
        popup_content.add_widget(title_label)
        popup_content.add_widget(title_input)

        # Add the content input (much bigger)
        content_input = TextInput(text=note_data["content"], multiline=True, size_hint_y=None, height=200)

        # Content label with proper alignment
        content_label = Label(text="Content:", size_hint_y=None, height=30, halign='left', valign='middle')

        # Add the content label and input vertically stacked
        popup_content.add_widget(content_label)
        popup_content.add_widget(content_input)

        # Create a delete button
        delete_button = Button(text="Delete Note", size_hint_y=None, height=50)
        delete_button.bind(on_press=lambda instance: self.delete_note(note_data))
        popup_content.add_widget(delete_button)

        # Create a save button
        save_button = Button(text="Save", size_hint_y=None, height=50)
        save_button.bind(on_press=lambda instance: self.save_note(note_data, title_input.text, content_input.text))
        popup_content.add_widget(save_button)

        # Create the popup
        self.popup = Popup(title="Edit Note", content=popup_content, size_hint=(0.8, 0.8))
        self.popup.open()


    def delete_note(self, note_data):
        # Remove the note from the list (assuming `self.notes` holds the notes)
        if note_data in self.notes:
            self.notes.remove(note_data)
            self.refresh_notes()  # Refresh the displayed notes after deletion
        self.popup.dismiss()  # Close the popup

    def save_note(self, note_data, title, content):
        # Update the note with the new title and content
        note_data["title"] = title
        note_data["content"] = content
        self.refresh_notes()  # Refresh the displayed notes after saving
        self.popup.dismiss()  # Close the popup

    def create_new_note(self, instance):
        new_note = {
            "title": "New Note",
            "date": datetime.now(),  # Use datetime object
            "content": ""  # Empty content initially
        }
        self.notes.insert(0, new_note)  # Insert at the top (most recent)
        self.refresh_notes()
        self.show_edit_popup(new_note)

    def toggle_sort_order(self, instance):
        # Toggle the sorting order and refresh notes
        if self.sort_order == 'chronological':
            self.sort_order = 'reverse'
        else:
            self.sort_order = 'chronological'

        # Refresh the notes with the updated sort order
        self.refresh_notes()

    def refresh_notes(self):
        # Clear and refresh the notes container (add all notes again)
        self.notes_container.clear_widgets()

        # Sort notes based on the current sort order
        if self.sort_order == 'chronological':
            sorted_notes = sorted(self.notes, key=lambda x: x['date'])
        else:
            sorted_notes = sorted(self.notes, key=lambda x: x['date'], reverse=True)

        # Add sorted notes back to the container
        for note in sorted_notes:
            self.notes_container.add_widget(self.create_note_widget(note))

        # Trigger a layout update by setting the height to None
        self.notes_container.height = self.notes_container.height

# Usage
# Initialize a list to hold the notes globally across popups
notes = []

# Create the popup with the current list of notes
popup = NotesPopup(notes)
popup.open()


# ----------------------
# Screens
# ----------------------

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        label = Label(
            text="Home Screen", 
            font_size=20, 
            color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'top': 0.99999}
        )
        layout.add_widget(label)

        # Floating Action Button
        fab = CircularButton(
            text="✍",
            font_name='DejaVuSans.ttf',
            pos_hint={'right': 0.95, 'y': 0.05},
            on_press=self.show_popup
        )
        layout.add_widget(fab)

        self.add_widget(layout)
        

    def show_popup(self, *args):
        popup = NotesPopup(notes)  # Pass 'notes' list here
        popup.open()


class CommunityScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Community Screen", font_size=20, color=(0, 0, 0, 1))
        layout.add_widget(label)
        self.add_widget(layout)


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Settings Screen", font_size=20, color=(0, 0, 0, 1))
        layout.add_widget(label)
        self.add_widget(layout)


# ----------------------
# Header
# ----------------------

class Header(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.1
        self.padding = 10
        self.orientation = 'horizontal'

        # Light gray background
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.add_widget(Label(
            text='[b]PRIMAL[/b]',
            markup=True,
            font_size=24,
            color=(0.2, 0.6, 0.86, 1)
        ))

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

# ----------------------
# Navigation Bar
# ----------------------

class NavBar(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.1
        self.orientation = 'horizontal'
        self.spacing = 10
        self.padding = [10, 5]

        # Light gray background
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.screen_manager = screen_manager

        # Buttons with the specified color
        button_color = (0.2, 0.6, 0.86, 1)  # Blue color

        self.home_btn = Button(
            text="Home", 
            background_normal='', 
            background_color=button_color, 
            on_press=lambda x: self.switch_screen("home")
        )
        self.community_btn = Button(
            text="Community", 
            background_normal='', 
            background_color=button_color, 
            on_press=lambda x: self.switch_screen("community")
        )
        self.settings_btn = Button(
            text="Settings", 
            background_normal='', 
            background_color=button_color, 
            on_press=lambda x: self.switch_screen("settings")
        )

        self.add_widget(self.home_btn)
        self.add_widget(self.community_btn)
        self.add_widget(self.settings_btn)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name


# ----------------------
# Root Layout
# ----------------------

class MobileRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_bg, pos=self.update_bg)

        self.header = Header()

        self.sm = ScreenManager(transition=FadeTransition(duration=0))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(CommunityScreen(name="community"))
        self.sm.add_widget(SettingsScreen(name="settings"))

        self.navbar = NavBar(self.sm)

        self.add_widget(self.header)
        self.add_widget(self.sm)
        self.add_widget(self.navbar)

    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos



# ----------------------
# App Entry Point
# ----------------------

class NotesApp(App):
    def build(self):
        return MobileRoot()


if __name__ == '__main__':
    NotesApp().run()
