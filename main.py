from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from nord_vpn_api.nord_client import NordClient


class MainApp(MDApp):
    nord_client = ObjectProperty()
    account_check_timer = ObjectProperty()

    def build(self):
        self.nord_client = NordClient()
        boxlayout = BoxLayout(orientation="vertical")
        self.login_button = MDRectangleFlatButton(text="login", halign="center")
        self.login_button.bind(on_press=self.login)
        boxlayout.add_widget(self.login_button)
        return boxlayout

    def login(self):
        self.nord_client.login(self.logged_in, self.login_fail)
        self.account_check_timer = Clock.schedule_interval(self.account_check, 1)

    def logged_in(self):
        self.login_button.text = "Logged in"

    def login_fail(self):
        self.login_button.text = "Login failed"

    def account_check(self, dt):
        if not self.nord_client.logged_in:
            self.nord_client.account(self.nord_client.check_login, self.login_fail)
        else:
            self.account_check_timer.cancel()


MainApp().run()