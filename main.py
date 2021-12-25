from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

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

    def handle_login(self):
        pass




MainApp().run()