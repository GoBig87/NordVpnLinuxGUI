from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy_garden.mapview import MapView, MapSource
from kivy.app import App
from kivymd.uix.label import MDLabel

from ui.widgets.status_box import StatusBox
from ui.widgets.country_selection import CountrySelection
from ui.constants import URL

Builder.load_string("""
<MapScreen>
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            padding: 0, dp(10)
            BoxLayout:
                orientation: "horizontal"
                size_hint_x: 0.2
                Widget:
            StatusBox:
                size_hint_x: 0.6
            BoxLayout:
                orientation: "horizontal"
                padding: dp(10), dp(10)
                size_hint_x: 0.2
                Widget:
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.9
            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                size_hint_x: 0.3
                MDBoxLayout:
                    id: selection
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
            BoxLayout:
                AnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    MapWidget:
                        zoom: 4
                        lat: 38.6394
                        lon: -100.057
    AnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(20), dp(20)
        MDFillRoundFlatButton:
            text: "Quick Connect"    
""")


class MapWidget(MapView):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.map_source = MapSource(url=URL, image_ext="png")


class MapScreen(Screen):
    map_source = MapSource(url=URL, image_ext="png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nord_client = App.get_running_app().nord_client
        self.build_country_list()

    def build_country_list(self):
        for country in self.nord_client.country_dict:
            self.ids.selection.add_widget(CountrySelection(country=country))
