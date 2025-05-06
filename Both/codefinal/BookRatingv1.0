#BookRating

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.base import EventLoop
from kivy.utils import platform

Window.size = (400, 700)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)

        self.layout.add_widget(MDLabel(text="Welcome to Book Rating App!", halign="center", font_style="H5"))
        self.layout.add_widget(MDRaisedButton(text="Rate a Book", pos_hint={"center_x": 0.5}, on_release=self.go_to_search))

        # Rewards
        self.reward_label = MDLabel(text="🏅 Rewards: None yet", halign="center", font_style="Subtitle1")
        self.layout.add_widget(self.reward_label)

        # Ratings section
        self.layout.add_widget(MDLabel(text="Previous Ratings:", halign="center", font_style="Subtitle1"))

        self.ratings_scroll = ScrollView()
        self.ratings_box = MDBoxLayout(orientation="vertical", size_hint_y=None, padding=10, spacing=10)
        self.ratings_box.bind(minimum_height=self.ratings_box.setter('height'))
        self.ratings_scroll.add_widget(self.ratings_box)
        self.layout.add_widget(self.ratings_scroll)

        self.add_widget(self.layout)

    def go_to_search(self, instance):
        self.manager.current = 'search'

    def update_previous_ratings(self):
        app = MDApp.get_running_app()
        self.ratings_box.clear_widgets()

        self.update_rewards_label(len(app.previous_ratings))

        if not app.previous_ratings:
            self.ratings_box.add_widget(MDLabel(text="No previous ratings yet.", halign="center"))
            return

        for index, rating in enumerate(app.previous_ratings):
            review_text = rating['review'] if rating['review'].strip() != "" else "(No review)"
            item_text = f"[b]{rating['book']}[/b]  ⭐{'⭐' * rating['stars']}\n{review_text}"
            item = MDBoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=100, padding=10)

            label = MDLabel(text=item_text, markup=True)

            delete_btn = MDIconButton(icon="delete", on_release=lambda x, idx=index: self.delete_rating(idx))
            share_btn = MDIconButton(icon="share-variant", on_release=lambda x, r=rating: self.share_rating(r))

            item.add_widget(label)
            item.add_widget(share_btn)
            item.add_widget(delete_btn)
            self.ratings_box.add_widget(item)

    def delete_rating(self, index):
        app = MDApp.get_running_app()
        if 0 <= index < len(app.previous_ratings):
            del app.previous_ratings[index]
            self.update_previous_ratings()

    def share_rating(self, rating):
        review_text = rating['review'] if rating['review'].strip() != "" else "(No review)"
        content = f"{rating['book']}\n⭐{'⭐' * rating['stars']}\n\n{review_text}"

        def copy_and_close(*_):
            Clipboard.copy(content)
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="Share Review",
            text=content,
            buttons=[
                MDFlatButton(text="Copy to Clipboard", on_release=copy_and_close),
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def update_rewards_label(self, count):
        reward = "🏅 Rewards: "
        if count >= 100:
            reward += "👑 Legendary Cup"
        elif count >= 50:
            reward += "🏆 Platinum Cup"
        elif count >= 25:
            reward += "🥇 Gold Cup"
        elif count >= 10:
            reward += "🥈 Silver Cup"
        elif count >= 5:
            reward += "🏆 Bronze Cup"
        elif count >= 1:
            reward += "🏅 Starter Cup"
        else:
            reward += "None yet"

        self.reward_label.text = reward


class SearchManagementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.books = [
            "The Great Gatsby", "To Kill a Mockingbird", "1984",
            "The Catcher in the Rye", "Pride and Prejudice", "Moby Dick",
            "Harry Potter", "The Hobbit", "The Lord of the Rings", "Jane Eyre"
        ]

        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=10)
        self.search_input = MDTextField(
            hint_text="Enter book title",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5}
        )
        self.search_input.bind(text=self.update_book_list)
        self.layout.add_widget(self.search_input)

        self.results_scroll = ScrollView()
        self.results_box = MDBoxLayout(orientation="vertical", size_hint_y=None)
        self.results_box.bind(minimum_height=self.results_box.setter('height'))
        self.results_scroll.add_widget(self.results_box)
        self.layout.add_widget(self.results_scroll)

        self.add_widget(self.layout)

    def update_book_list(self, instance, value):
        self.results_box.clear_widgets()
        for book in self.books:
            if value.lower() in book.lower():
                item = OneLineListItem(text=book, on_release=self.select_book)
                self.results_box.add_widget(item)

    def select_book(self, instance):
        selected_book = instance.text
        app = MDApp.get_running_app()
        app.selected_book = selected_book
        self.manager.current = 'rating_form'


class ReviewPageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=15)
        self.layout.add_widget(MDLabel(text="Rate the Book", halign="center", font_style="H6"))

        self.star_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        self.stars = []

        for i in range(5):
            star = MDIconButton(icon="star-outline", theme_text_color="Custom", text_color=(1, 0.7, 0), on_release=self.set_rating)
            self.stars.append(star)
            self.star_layout.add_widget(star)

        self.layout.add_widget(self.star_layout)

        # Formatting buttons for review text
        self.format_buttons_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        self.bold_btn = MDRaisedButton(text="Bold", on_release=self.set_bold)
        self.italic_btn = MDRaisedButton(text="Italic", on_release=self.set_italic)
        self.bullet_btn = MDRaisedButton(text="Bullet", on_release=self.set_bullet)
        self.format_buttons_layout.add_widget(self.bold_btn)
        self.format_buttons_layout.add_widget(self.italic_btn)
        self.format_buttons_layout.add_widget(self.bullet_btn)

        self.layout.add_widget(self.format_buttons_layout)

        self.review_input = MDTextField(
            hint_text="Write your review (optional)", multiline=True, size_hint_y=0.4
        )
        self.layout.add_widget(self.review_input)

        self.layout.add_widget(MDRaisedButton(text="Next", pos_hint={"center_x": 0.5}, on_release=self.go_to_preview))
        self.add_widget(self.layout)

    def set_rating(self, instance):
        index = self.stars.index(instance)
        app = MDApp.get_running_app()
        app.rating_value = index + 1

        for i, star in enumerate(self.stars):
            star.icon = "star" if i <= index else "star-outline"

    def go_to_preview(self, instance):
        app = MDApp.get_running_app()
        app.review_text = self.review_input.text
        self.manager.current = 'preview'

    def set_bold(self, instance):
        app = MDApp.get_running_app()
        review = self.review_input.text
        self.review_input.text = f"[b]{review}[/b]"

    def set_italic(self, instance):
        app = MDApp.get_running_app()
        review = self.review_input.text
        self.review_input.text = f"[i]{review}[/i]"

    def set_bullet(self, instance):
        app = MDApp.get_running_app()
        review = self.review_input.text
        self.review_input.text = f"• {review}"


class ReviewPreviewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anonymous = False
        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=15)
        self.label = MDLabel(halign="center", font_style="Body1")
        self.layout.add_widget(MDLabel(text="Preview Your Review", halign="center", font_style="H6"))
        self.layout.add_widget(self.label)

        self.checkbox = MDCheckbox()
        self.checkbox.bind(active=self.toggle_anonymous)
        self.layout.add_widget(MDLabel(text="Post Anonymously?", halign="center"))
        self.layout.add_widget(self.checkbox)

        self.layout.add_widget(MDRaisedButton(text="Publish", pos_hint={"center_x": 0.5}, on_release=self.publish))
        self.add_widget(self.layout)

    def on_enter(self):
        app = MDApp.get_running_app()
        stars = "⭐" * app.rating_value
        book = app.selected_book
        review = app.review_text if app.review_text.strip() != "" else "(No review text provided)"
        self.label.text = f"[b]{book}[/b]\n\n{stars}\n\n{review}"

    def toggle_anonymous(self, checkbox, value):
        self.anonymous = value

    def publish(self, instance):
        app = MDApp.get_running_app()
        app.previous_ratings.append({
            'book': app.selected_book,
            'stars': app.rating_value,
            'review': app.review_text,
            'anonymous': self.anonymous
        })
        self.manager.current = 'confirmation'


class SearchResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(MDLabel(text="Review Published Successfully! 🎉", halign="center", font_style="H6"))
        layout.add_widget(MDRaisedButton(text="Back to Home", pos_hint={"center_x": 0.5}, on_release=self.go_home))
        self.add_widget(layout)

    def go_home(self, instance):
        home_screen = self.manager.get_screen('home')
        home_screen.update_previous_ratings()
        self.manager.current = 'home'


class CustomerApp(MDApp):
    def build(self):
        self.review_text = ""
        self.rating_value = 3
        self.selected_book = ""
        self.previous_ratings = []
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='home'))
        self.sm.add_widget(SearchManagementScreen(name='search'))
        self.sm.add_widget(ReviewPageScreen(name='rating_form'))
        self.sm.add_widget(ReviewPreviewScreen(name='preview'))
        self.sm.add_widget(SearchResultScreen(name='confirmation'))
        return self.sm

    def on_start(self):
        if platform in ('android', 'win', 'linux', 'macos', 'ios'):
            EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *args):
        if key == 27:
            if self.sm.current != 'home':
                self.sm.transition.direction = 'right'
                self.sm.current = 'home'
                return True
            return False


if __name__ == '__main__':
    CustomerApp().run()
