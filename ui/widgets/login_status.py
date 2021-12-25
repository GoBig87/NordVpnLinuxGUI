from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

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
        size_hint_x: 0.15
        icon: root.login_icon
        font_size: 40
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        valign: "center"
    MDFlatButton:
        id: login_label
        text: root.login_text
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0, 'center_y': .5}
    Widget:
        size_hint_x: 0.2
""")

class LoginStatus(BoxLayout):
    login_icon = StringProperty("login")
    login_text = StringProperty("Login")

    def __init__(self, **kwargs):
        super(LoginStatus, self).__init__(**kwargs)

    def set_logged_out(self):
        self.login_text = "Login"
        self.login_icon = "login"

    def set_logged_in(self):
        self.login_text = "Log out"
        self.login_icon = "logout"