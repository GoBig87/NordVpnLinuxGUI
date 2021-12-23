from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, NoTransition

from nord_vpn_api.nord_client import NordClient
from ui.screens.map_screen import MapScreen

class MainApp(MDApp):
    nord_client = ObjectProperty(NordClient())

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.mainbox = FloatLayout()
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')

        self.content = ScreenManager()
        self.content.transition = NoTransition()
        self.content.add_widget(MapScreen())
        self.screens.add_widget(self.content)
        self.mainbox.add_widget(self.screens)
        return self.mainbox

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