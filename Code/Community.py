from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior

from datetime import datetime


Window.size = (360, 640)  # Simulate a mobile device


# ----------------------
# Screens
# ----------------------

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Home Screen", font_size=20, color=(0, 0, 0, 1))
        layout.add_widget(label)
        self.add_widget(layout)


class CommunityScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.active_main_screen = "posts"  # Default

        root = FloatLayout()

        # Vertical layout for header and scrollable post area
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # Top bar layout for Menu and Friends buttons
        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(40),
            padding=[dp(10), 0, dp(10), 0],  # optional padding: [left, top, right, bottom]
            spacing=dp(10)
        )

        # Menu button (left)
        self.menu_button = Button(
            text="≡",
            font_name='DejaVuSans.ttf',
            size_hint=(None, 1),
            width=dp(30),
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1)
        )
        self.menu_button.bind(on_press=self.open_categories)  # Define this method
        top_bar.add_widget(self.menu_button)

        # Spacer to push the Friends button to the right
        top_bar.add_widget(Widget())

        # Friends button (right)
        self.header_button = Button(
            text="Friends",
            size_hint=(None, 1),
            width=dp(68),
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1)
        )
        self.header_button.bind(on_press=self.open_friends_list_popup)
        top_bar.add_widget(self.header_button)

        # Add the top bar to the main layout
        self.layout.add_widget(top_bar)

        # Scrollable post area
        self.post_scroll = ScrollView(size_hint=(1, 0.85))
        self.post_area = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(10))
        self.post_area.bind(minimum_height=self.post_area.setter('height'))
        self.post_scroll.add_widget(self.post_area)
        self.layout.add_widget(self.post_scroll)

        # Floating action button
        self.fab = Button(
            text="+",
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1),
            font_size=32,
            pos_hint={'right': 0.96, 'y': 0.02}
        )
        self.fab.bind(on_press=self.open_create_post_popup)
        self.make_circular(self.fab)

        root.add_widget(self.layout)
        root.add_widget(self.fab)
        self.add_widget(root)

    def update_header_rect(self, instance, *args):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def make_circular(self, widget):
        widget.canvas.before.clear()
        with widget.canvas.before:
            Color(*widget.background_color)
            self.ellipse = RoundedRectangle(size=widget.size, pos=widget.pos, radius=[dp(28)])
        widget.bind(size=self.update_ellipse, pos=self.update_ellipse)

    def update_ellipse(self, instance, *args):
        self.ellipse.size = instance.size
        self.ellipse.pos = instance.pos

    def open_create_post_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        text_input = TextInput(hint_text="Write your post...", multiline=True)
        submit_btn = Button(text="Post", size_hint_y=None, height=40)

        popup = Popup(title="Create Post", content=content, size_hint=(0.9, 0.5))
        content.add_widget(text_input)
        content.add_widget(submit_btn)

        submit_btn.bind(on_press=lambda *args: self.create_post(text_input.text, popup))
        popup.open()

    def create_post(self, text, popup):
        if text.strip() == "":
            return

        user_name = "You"  # Replace with actual user if applicable
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Post container
        post_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(140), padding=dp(10), spacing=dp(5))
        post_box.size_hint_x = 0.95
        post_box.pos_hint = {'center_x': 0.5}
        with post_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            post_box.bg = RoundedRectangle(radius=[10], pos=post_box.pos, size=post_box.size)
        post_box.bind(pos=self.update_box_bg, size=self.update_box_bg)

        # Post header (name + time)
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20))
        name_label = Label(text=f"[b]{user_name}[/b]", markup=True, color=(0.2, 0.2, 0.2, 1), halign='left', valign='middle')
        time_label = Label(text=timestamp, color=(0.5, 0.5, 0.5, 1), font_size=12, halign='right', valign='middle')
        name_label.bind(size=name_label.setter('text_size'))
        time_label.bind(size=time_label.setter('text_size'))
        header.add_widget(name_label)
        header.add_widget(time_label)

        post_box.time_label = time_label  # Store reference to the time label for later use

        # Text content
        post_label = Label(
            text=text,
            halign='left',
            valign='top',  # Align the text at the top
            size_hint_y=None,  # Allow the label to expand based on content
            height=self.calculate_text_height(text),  # Dynamically set height based on text content
            color=(0.1, 0.1, 0.1, 1)
        )
        post_label.bind(size=post_label.setter('text_size'))  # Bind the size of the text

        # Like button and counter
        self.like_count = 0  # Initialize like count for this post
        like_btn = Button(
            text=f"♡ ({self.like_count})",
            font_name='DejaVuSans.ttf',
            size_hint=(None, None),
            size=(dp(60), dp(40)),
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1)
        )
        like_btn.bind(on_press=lambda inst: self.like_post(inst, post_label))

        # Comment button
        comment_btn = Button(
            text="➤",
            font_name='DejaVuSans.ttf',
            size_hint=(None, None),
            size=(dp(30), dp(40)),
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1)
        )
        comment_btn.bind(on_press=lambda inst: self.comment_post(post_label))  # Bind to comment_post

        # Share button
        share_btn = Button(
            text="✈",
            font_name='DejaVuSans.ttf',
            size_hint=(None, None),
            size=(dp(30), dp(40)),
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1)
        )
        share_btn.bind(on_press=lambda inst: self.share_post(post_label))  # Bind to comment_post

        # Action button (⋮)
        action_btn = Button(
            text="⋮",
            font_name='DejaVuSans.ttf',
            size_hint=(None, None),
            size=(dp(30), dp(40)),
            background_normal='',
            background_color=(0.2, 0.4, 0.46, 1),
            color=(1, 1, 1, 1)
        )
        action_btn.bind(on_press=lambda inst: self.open_post_options(post_label, post_box))

        # Comment List button (Initially hidden)
        comment_list_btn = Button(
            text="Comments",
            size_hint=(None, None),
            size=(dp(90), dp(40)),
            background_normal='',
            background_color=(0.0, 0.6, 0.86, 1),
            color=(1, 1, 1, 1),
            opacity=0  # Initially hidden
        )
        comment_list_btn.bind(on_press=lambda inst: self.view_comments(post_box))

        # Horizontal layout for Like, Comment, Share, Action and Comment List buttons 
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        buttons_layout.add_widget(like_btn)
        buttons_layout.add_widget(comment_btn)
        buttons_layout.add_widget(share_btn)
        buttons_layout.add_widget(action_btn)
        buttons_layout.add_widget(comment_list_btn)  # Add the comment list button

        # Assemble post components
        post_box.add_widget(header)
        post_box.add_widget(post_label)
        post_box.add_widget(buttons_layout)

        self.post_area.add_widget(post_box, index=0)  # Add to the top
        popup.dismiss()

        # Store the comment list and button reference
        post_box.comment_list_btn = comment_list_btn
        post_box.comments = []  # Initialize an empty list of comments

        # Dynamically calculate the height of the entire post
        header_height = dp(20)
        buttons_height = dp(40)
        spacing = post_box.spacing * 2  # spacing between header, post_label, and buttons
        padding = post_box.padding[1] * 2  # vertical padding

        post_box.height = header_height + post_label.height + buttons_height + spacing + padding

        # Allow post_box to expand infinitely
        post_box.size_hint_y = None  # Remove any height constraints

        # Update the background size
        post_box.bg.size = post_box.size
        post_box.bg.pos = post_box.pos
        self.update_box_bg(post_box, post_box.size)
        

    def calculate_text_height(self, text):
        # Dynamically calculate the height of the text based on the content
        # The assumption is that a line of text takes up a height of dp(20)
        # Adjust this depending on the font size and style you're using.
        lines = text.split('\n')
        return dp(20) * len(lines)

    def update_box_bg(self, instance, value):
        # Update the background size to match the box size
        instance.bg.pos = instance.pos
        instance.bg.size = instance.size

    def like_post(self, like_btn, post_label):
        # Toggle like state and update the counter
        if self.like_count == 0:
            self.like_count += 1
            like_btn.text = f"♥ ({self.like_count})"
            # You could change the button color to indicate it's liked
            like_btn.background_color = (0.4, 0.8, 0.4, 1)  # Liked color (green-ish)
        else:
            self.like_count -= 1
            like_btn.text = f"♡ ({self.like_count})"
            # Reset button color
            like_btn.background_color = (0.2, 0.6, 0.86, 1)  # Default color

    def comment_post(self, post_label):
        # Create a comment popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create the text input for the comment
        text_input = TextInput(hint_text="Write your comment...", multiline=True, size_hint_y=None, height=dp(100))

        # Create the submit button
        submit_btn = Button(text="Submit", size_hint_y=None, height=dp(40))

        # Create the pop-up and open it
        popup = Popup(title="Add Comment", content=content, size_hint=(0.9, 0.5))
        content.add_widget(text_input)
        content.add_widget(submit_btn)

        submit_btn.bind(on_press=lambda *args: self.submit_comment(post_label, text_input.text, popup))
        popup.open()

        
    def share_post(self, post_label):
        # Placeholder for share functionality
        print(f"Share post?")
        return


    def submit_comment(self, post_label, comment_text, popup):
        if comment_text.strip() == "":
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        comment_text_full = f"[b]You[/b]: {comment_text} \n[i]Posted at {timestamp}[/i]"

        post_label.parent.comments.append({
            "text": comment_text_full,
            "likes": 0,
            "liked": False
        })

        # Show the button if there is at least one comment
        post_label.parent.comment_list_btn.opacity = 1
        post_label.parent.comment_list_btn.disabled = False

        popup.dismiss()


    def create_comment_widget(self, text):
        comment_label = Label(
            text=text,
            markup=True,
            halign='left',
            valign='top',
            size_hint_y=None,
            color=(0.1, 0.1, 0.1, 1),
            padding=(dp(10), dp(10)),
        )
        comment_label.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )
        comment_label.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1])
        )
        return comment_label


    def view_comments(self, post_box):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        with content.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self.update_rect, pos=self.update_rect)

        from kivy.uix.scrollview import ScrollView
        scroll_view = ScrollView(size_hint=(1, 1))

        comment_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(5))
        comment_layout.bind(minimum_height=comment_layout.setter('height'))

        for comment_data in reversed(post_box.comments):
            wrapper = BoxLayout(orientation='vertical', size_hint_y=None, padding=(0, dp(5)))
            wrapper.bind(minimum_height=wrapper.setter('height'))

            comment_text = comment_data["text"]
            like_count = comment_data.get("likes", 0)
            liked = comment_data.get("liked", False)

            comment_label = self.create_comment_widget(comment_text)
            wrapper.add_widget(comment_label)

            like_btn = Button(
                text=f"{'♥' if liked else '♡'} ({like_count})",
                font_name='DejaVuSans.ttf',
                size_hint=(None, None),
                size=(dp(45), dp(30)),
                background_color=(0.4, 0.8, 0.4, 1) if liked else (0.2, 0.6, 0.86, 1),
                color=(1, 1, 1, 1),
                font_size=dp(12)
            )

            def like_comment(instance, btn=like_btn, data=comment_data):
                if data["liked"]:
                    data["likes"] -= 1
                    data["liked"] = False
                    btn.text = f"♡ ({data['likes']})"
                    btn.background_color = (0.2, 0.6, 0.86, 1)
                else:
                    data["likes"] += 1
                    data["liked"] = True
                    btn.text = f"♥ ({data['likes']})"
                    btn.background_color = (0.4, 0.8, 0.4, 1)

            like_btn.bind(on_press=like_comment)

            # Create the Delete Button
            delete_btn = Button(
                text="Delete",
                size_hint=(None, None),
                size=(dp(80), dp(30)),
                background_color=(1, 0.3, 0.3, 1),
                font_size=dp(12)
            )

            # Function to delete comment
            def delete_comment(instance, comment_ref=comment_data, wrapper_ref=wrapper):
                if comment_ref in post_box.comments:
                    post_box.comments.remove(comment_ref)
                if wrapper_ref.parent:
                    wrapper_ref.parent.remove_widget(wrapper_ref)
                if len(post_box.comments) == 0:
                    post_box.comment_list_btn.opacity = 0
                    post_box.comment_list_btn.disabled = True
                    popup.dismiss()

            # Bind the delete button to the delete function
            delete_btn.bind(on_press=delete_comment)

            # Horizontal layout for like and delete buttons
            button_row = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(30))
            button_row.add_widget(like_btn)
            button_row.add_widget(delete_btn)
            wrapper.add_widget(button_row)

            comment_layout.add_widget(wrapper)

        scroll_view.add_widget(comment_layout)
        content.add_widget(scroll_view)

        popup = Popup(title="Comments", content=content, size_hint=(0.8, 0.6))
        popup.open()


    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


    def open_post_options(self, post_label, post_box):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Set background color to light grey for the popup
        with content.canvas.before:
            content.bg = RoundedRectangle(pos=content.pos, size=content.size, radius=[10])

        # Center the buttons vertically and horizontally
        options_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(160), dp(100)), padding=dp(10), spacing=dp(10))
        options_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Edit and Delete buttons
        edit_btn = Button(
            text="Edit", 
            size_hint=(None, None), 
            size=(dp(80), dp(40)), 
            background_normal='', 
            background_color=(0.2, 0.6, 0.86, 1), 
            color=(1, 1, 1, 1)
        )
        delete_btn = Button(
            text="Delete", 
            size_hint=(None, None), 
            size=(dp(80), dp(40)), 
            background_normal='', 
            background_color=(0.2, 0.6, 0.86, 1), 
            color=(1, 1, 1, 1)
        )

        options_layout.add_widget(edit_btn)
        options_layout.add_widget(delete_btn)

        # Create and show the popup
        popup = Popup(title="Post Options", content=options_layout, size_hint=(0.8, 0.4))
        edit_btn.bind(on_press=lambda *args: self.edit_post(post_label, popup))
        delete_btn.bind(on_press=lambda *args: self.delete_post(post_box, popup))

        popup.open()

    def edit_post(self, post_label, popup):
        popup.dismiss()
        
        # Create a new popup to edit the post
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        text_input = TextInput(text=post_label.text, multiline=True)
        
        # Save button to save the edited post
        save_btn = Button(
            text="Save", 
            size_hint_y=None, 
            height=40, 
            background_normal='', 
            background_color=(0.2, 0.6, 0.86, 1), 
            color=(1, 1, 1, 1)
        )

        # Create the popup for editing the post
        edit_popup = Popup(title="Edit Post", content=content, size_hint=(0.9, 0.5))
        content.add_widget(text_input)
        content.add_widget(save_btn)

        # When the save button is pressed, save the edited post and update the layout
        save_btn.bind(on_press=lambda *args: self.save_edited_post(post_label, text_input.text, edit_popup))

        edit_popup.open()

    def save_edited_post(self, post_label, new_text, edit_popup):
        # Save the new text to the post label
        post_label.text = new_text

        # Recalculate the height of the post box and text
        post_box = post_label.parent
        post_label.height = self.calculate_text_height(new_text)

        # Update the post box height to reflect the updated content size
        header_height = dp(20)
        buttons_height = dp(40)
        spacing = post_box.spacing * 2
        padding = post_box.padding[1] * 2

        post_box.height = header_height + post_label.height + buttons_height + spacing + padding
        post_box.size_hint_y = None

        # Directly access the stored time label reference
        edited_timestamp = datetime.now().strftime("Edited: %Y-%m-%d %H:%M")
        post_box.time_label.text = edited_timestamp

        # Update the background size
        post_box.bg.size = post_box.size
        post_box.bg.pos = post_box.pos

        # Refresh layout
        self.update_box_bg(post_box, post_box.size)

        # Close the popup
        edit_popup.dismiss()


    def delete_post(self, post_box, popup):
        popup.dismiss()
        self.post_area.remove_widget(post_box)

    class ClickableBox(ButtonBehavior, BoxLayout):
        pass

    def open_friends_list_popup(self, instance):
        # Create a screen manager to hold multiple views
        screen_manager = ScreenManager(transition=SlideTransition(duration=0.3))

        # --------- Screen 1: Friend List ----------
        friend_screen = Screen(name='friends')

        friend_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Top bar with "+" button
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(5))
        top_bar.add_widget(Label(text="Friends", color=(0, 0, 0, 1)))

        add_btn = Button(text="+", size_hint=(None, 1), width=dp(40), background_color=(0.3, 0.6, 1, 1))
        top_bar.add_widget(add_btn)

        friend_layout.add_widget(top_bar)

        # Scrollable friend list
        scroll_view = ScrollView()
        friend_list = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(5))
        friend_list.bind(minimum_height=friend_list.setter('height'))

        class ClickableBox(ButtonBehavior, BoxLayout):
            pass

        for friend in self.get_friends():
            def create_placeholder_picture():
                pic = Widget(size_hint=(None, None), size=(dp(40), dp(40)))
                with pic.canvas:
                    Color(0.9, 0.9, 0.9, 1)
                    ellipse = Ellipse(pos=pic.pos, size=pic.size)

                def update_ellipse(instance, *args):
                    ellipse.pos = instance.pos
                    ellipse.size = instance.size

                pic.bind(pos=update_ellipse, size=update_ellipse)
                return pic

            clickable_box = ClickableBox(orientation='vertical', size_hint_y=None, height=dp(100), padding=dp(5), spacing=dp(5))
            friend_box_canvas = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))

            pic = create_placeholder_picture()
            name_status = BoxLayout(orientation='vertical', spacing=dp(2), size_hint=(1, None), height=dp(40))
            name_label = Label(
                text=friend['name'],
                size_hint_y=None,
                height=dp(20),
                color=(0, 0, 0, 1),
                halign='left',
                valign='middle'
            )
            status_label = Label(
                text=friend.get('status', 'Online'),
                size_hint_y=None,
                height=dp(20),
                color=(0.4, 0.4, 0.4, 1),
                halign='left',
                valign='middle'
            )
            name_label.bind(size=name_label.setter('text_size'))
            status_label.bind(size=status_label.setter('text_size'))
            name_status.add_widget(name_label)
            name_status.add_widget(status_label)

            friend_box_canvas.add_widget(pic)
            friend_box_canvas.add_widget(name_status)

            activity_label = Label(
                text=f"{friend['activity']}",
                size_hint_y=None,
                height=dp(20),
                color=(0.3, 0.3, 0.3, 1),
                halign='left',
                valign='top'
            )
            activity_label.bind(size=activity_label.setter('text_size'))

            clickable_box.add_widget(friend_box_canvas)
            clickable_box.add_widget(activity_label)

            # Make the whole box open popup
            clickable_box.bind(on_press=lambda inst, name=friend['name']: self.open_friend_popup(name))

            friend_list.add_widget(clickable_box)

        scroll_view.add_widget(friend_list)
        friend_layout.add_widget(scroll_view)

        friend_screen.add_widget(friend_layout)
        screen_manager.add_widget(friend_screen)    

        # --------- Screen 2: Search Users ----------
        search_screen = Screen(name='search')

        search_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        back_btn = Button(text="< Back", size_hint_y=None, height=dp(40), background_color=(0.8, 0.2, 0.2, 1))
        

        search_input = TextInput(hint_text="Search users...", size_hint_y=None, height=dp(40))

        search_input = TextInput(hint_text="Search users...", size_hint_y=None, height=dp(40))

        user_results_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(5))
        user_results_layout.bind(minimum_height=user_results_layout.setter('height'))

        scroll_results = ScrollView(size_hint=(1, 1))
        scroll_results.add_widget(user_results_layout)

        def update_search_results(instance, value):
            search_query = value.strip().lower()
            all_users = self.get_all_users()
            user_results_layout.clear_widgets()

            if not search_query:
                return

            matches = [user for user in all_users if search_query in user.lower()]

            for user_name in matches:
                user_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))

                # Placeholder circle
                def create_placeholder_pic():
                    pic = Widget(size_hint=(None, None), size=(dp(40), dp(40)))
                    with pic.canvas:
                        Color(0.85, 0.85, 0.85, 1)
                        ellipse = Ellipse()

                    def update_ellipse(instance, *args):
                        ellipse.pos = instance.pos
                        ellipse.size = instance.size

                    pic.bind(pos=update_ellipse, size=update_ellipse)
                    return pic

                pic = create_placeholder_pic()

                name_btn = Button(
                    text=user_name,
                    size_hint=(1, None),
                    height=dp(40),
                    background_color=(0, 0, 0, 0),
                    background_normal='',
                    color=(0, 0, 0, 1),
                    halign='left',
                    valign='middle',
                )

                name_btn.bind(on_press=lambda btn, uname=user_name: self.show_user_popup(uname))

                user_box.add_widget(pic)
                user_box.add_widget(name_btn)
                user_results_layout.add_widget(user_box)

        search_input.bind(text=update_search_results)

        search_layout.add_widget(back_btn)
        search_layout.add_widget(search_input)
        search_layout.add_widget(scroll_results)

        search_screen.add_widget(search_layout)
        screen_manager.add_widget(search_screen)

        # --------- Bind Buttons ----------
        add_btn.bind(on_press=lambda x: setattr(screen_manager, 'current', 'search'))
        back_btn.bind(on_press=lambda x: setattr(screen_manager, 'current', 'friends'))

        # --------- Final Popup ----------
        popup = Popup(
            title="My Friends",
            content=screen_manager,
            size_hint=(0.85, 0.75),
            background='',
            background_color=(1, 1, 1, 1),
            separator_color=(0.7, 0.7, 0.7, 1),
            title_color=(0, 0, 0, 1)
        )
        popup.open()


    def open_friend_popup(self, user_name):
            layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
            layout.add_widget(Label(text=f"{user_name}", font_size=dp(20), color=(0, 0, 0, 1)))
            layout.add_widget(Label(text="Additional info here...", font_size=dp(16), color=(0.3, 0.3, 0.3, 1)))


            popup = Popup(
                title=f"Profile: {user_name}",
                content=layout,
                size_hint=(0.7, 0.5),
                background='',
                background_color=(1, 1, 1, 1),
                separator_color=(0.7, 0.7, 0.7, 1),
                title_color=(0, 0, 0, 1)
            )
            popup.open()


    def show_user_popup(self, username):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        info_label = Label(
            text=f"[b]{username}[/b]\nStatus: Unknown\nBio: Just another user.",
            markup=True,
            size_hint_y=None,
            height=dp(100),
            color=(0, 0, 0, 1),
            halign='left',
            valign='top'
        )
        info_label.bind(size=info_label.setter('text_size'))

        add_btn = Button(
            text="Add Friend",
            size_hint_y=None,
            height=dp(40),
            background_color=(0.3, 0.7, 0.3, 1),
            color=(1, 1, 1, 1)
        )

        def add_friend(instance):
            print(f"Friend request sent to {username}")
            user_popup.dismiss()

        add_btn.bind(on_press=add_friend)

        content.add_widget(info_label)
        content.add_widget(add_btn)

        user_popup = Popup(
            title=f"{username}'s Profile",
            content=content,
            size_hint=(0.7, 0.4),
            title_color=(0, 0, 0, 1),
            background='',
            background_color=(1, 1, 1, 1),
            separator_color=(0.7, 0.7, 0.7, 1)
        )

        user_popup.open()


    def get_friends(self):
        return [
            {"name": "Alice", "status": "Online", "activity": "Posted a photo"},
            {"name": "Bob", "status": "Away", "activity": "Liking posts"},
            {"name": "Charlie", "status": "Offline", "activity": "Commented on your post"},
            {"name": "David", "status": "Busy", "activity": "Updated status"},
        ]
    

    def get_all_users(self):
        return [
            "Alice", "Bob", "Charlie", "David", "Emma",
            "Frank", "Grace", "Alice", "Henry", "Emma"
        ]

    def open_categories(self, instance):
        # Placeholder for menu functionality
        print("Categories button pressed")
        return



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

class CommunityApp(App):
    def build(self):
        return MobileRoot()


if __name__ == '__main__':
    CommunityApp().run()
