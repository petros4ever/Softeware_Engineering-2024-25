from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class PostManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.posts = []

        # Input field
        self.input = TextInput(hint_text="Write a post...", size_hint_y=None, height=100)
        self.add_widget(self.input)

        # Button row
        button_row = BoxLayout(size_hint_y=None, height=50)
        self.add_btn = Button(text="Add Post")
        self.add_btn.bind(on_press=self.add_post)
        button_row.add_widget(self.add_btn)
        self.add_widget(button_row)

        # Scrollable area for posts
        self.post_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.post_layout.bind(minimum_height=self.post_layout.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.post_layout)
        self.add_widget(scroll)

    def add_post(self, instance):
        content = self.input.text.strip()
        if content:
            self.posts.append(content)
            self.input.text = ""
            self.refresh_posts()

    def refresh_posts(self):
        self.post_layout.clear_widgets()
        for i, post in enumerate(self.posts):
            post_box = BoxLayout(size_hint_y=None, height=60)
            post_label = Label(text=post, halign='left', valign='middle')
            post_label.bind(size=post_label.setter('text_size'))

            edit_btn = Button(text="Edit", size_hint_x=None, width=80)
            delete_btn = Button(text="Delete", size_hint_x=None, width=80)

            edit_btn.bind(on_press=lambda inst, idx=i: self.edit_post(idx))
            delete_btn.bind(on_press=lambda inst, idx=i: self.delete_post(idx))

            post_box.add_widget(post_label)
            post_box.add_widget(edit_btn)
            post_box.add_widget(delete_btn)

            self.post_layout.add_widget(post_box)

    def edit_post(self, index):
        self.input.text = self.posts[index]
        self.add_btn.text = "Update Post"
        self.add_btn.unbind(on_press=self.add_post)
        self.add_btn.bind(on_press=lambda instance: self.update_post(index))

    def update_post(self, index):
        new_content = self.input.text.strip()
        if new_content:
            self.posts[index] = new_content
            self.input.text = ""
            self.refresh_posts()
            self.add_btn.text = "Add Post"
            self.add_btn.unbind(on_press=self.update_post)
            self.add_btn.bind(on_press=self.add_post)

    def delete_post(self, index):
        del self.posts[index]
        self.refresh_posts()


class PostApp(App):
    def build(self):
        return PostManager()


if __name__ == '__main__':
    PostApp().run()
