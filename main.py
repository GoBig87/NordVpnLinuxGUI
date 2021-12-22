from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from nord_vpn_api.nord_client import NordClient


class MainApp(MDApp):
    def build(self):
        self.nord_client = NordClient()
        boxlayout = BoxLayout(orientation="vertical")
        self.login_button = MDRectangleFlatButton(text="login")
        self.login_button.bind(on_press=self.login)
        boxlayout.add_widget(self.login_button)
        return boxlayout

    def login(self, instance):
        self.nord_client.login(self.nord_client.login_success, self.login_fail)
        self.account_check_timer = Clock.schedule_interval(self.account_check, 1)

    def logged_in(self, output):
        self.login_button.text = "Logging in..."

    def login_fail(self, output):
        self.login_button.text = "Login failed"

    def account_check(self, dt):
        print("Checking account....")
        if not self.nord_client.logged_in:
            print("not logged in...")
            self.nord_client.account(self.nord_client.check_login, self.login_fail)
        else:
            print("canceling timer")
            self.account_check_timer.cancel()


MainApp().run()