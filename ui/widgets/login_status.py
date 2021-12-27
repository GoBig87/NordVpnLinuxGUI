from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel

from ui.widgets.label_button import LabelButton

Builder.load_string("""
<LoginStatus>
    id: login_status
    orientation: "horizontal"
    padding: dp(10), dp(10)
    Widget:
        size_hint_x: 0.2
    MDIcon:
        id: login_icon
        size_hint_x: 0.25
        icon: root.login_icon
        font_size: 40
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        valign: "center"
    BoxLayout:
        id: email_box
        orientation: "vertical"
        spacing: dp(18)
        MDLabel:
            id: login_label
            text: root.login_text
            font_style: "Subtitle1"
            font_size: 16
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            bold: True
""")

class LoginStatus(ButtonBehavior, BoxLayout):
    login_icon = StringProperty("login")
    login_text = StringProperty("Login")
    email = StringProperty("")

    def __init__(self, **kwargs):
        super(LoginStatus, self).__init__(**kwargs)

    def set_logged_out(self):
        self.login_text = "Login"
        self.login_icon = "login"
        widget = self.ids.email_box.children[0]
        self.ids.email_box.remove_widget(widget)

    def set_logged_in(self, email):
        self.email = email
        self.login_text = "Log out"
        self.login_icon = "logout"
        label = MDLabel(text=self.email,
                        font_style="Subtitle1",
                        font_size=12)
        self.ids.email_box.add_widget(label)
