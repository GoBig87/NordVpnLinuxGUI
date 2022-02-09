from kivy.config import Config

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, NoTransition

from nord_vpn_api.nord_client import NordClient
from ui.screens.map_screen import MapScreen
from ui.screens.settings_screen import SettingsScreen
from ui.widgets.status_dialog import StatusDialog


class MainApp(MDApp):
    nord_client = ObjectProperty()

    def build(self):
        self.status_dialog = StatusDialog()
        self.status_dialog.on_dismiss = self.on_dismiss
        self.nord_client = NordClient(self.error_dialog_cb)
        self.theme_cls.theme_style = "Dark"
        self.mainbox = FloatLayout()
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')

        self.content = ScreenManager()
        self.content.transition = NoTransition()
        self.content.add_widget(MapScreen(name="map"))
        self.content.add_widget(SettingsScreen(name="settings"))
        self.screens.add_widget(self.content)
        self.mainbox.add_widget(self.screens)

        return self.mainbox

    def handle_login(self):
        pass

    def error_dialog_cb(self, title, error):
        error_rsp = f"{title} {error}"
        self.status_dialog.open_error(error_rsp)

    def on_dismiss(self, *args):
        self.nord_client = NordClient(self.error_dialog_cb)



MainApp().run()