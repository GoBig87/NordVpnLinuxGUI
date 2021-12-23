from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy_garden.mapview import MapView, MapSource

from ui.widgets.proctection_status import ProtectionStatus
from ui.widgets.location_status import LocationStatus

URL = "https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"

Builder.load_string("""
<MapScreen>
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            MDBoxLayout:
                orientation: "horizontal"
                size_hint_x: 0.3
                Widget:
            MDBoxLayout:
                orientation: "horizontal"
                size_hint_x: 0.6
                ProtectionStatus:
                LocationStatus:
                MDLabel:
                    text: "Help"
            MDBoxLayout:
                orientation: "horizontal"
                padding: dp(10), dp(10)
                size_hint_x: 0.2
                MDRectangleFlatButton:
                    text: "Quick Connect"
        MDBoxLayout:
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
                    Label:
                        size_hint: (1, None)
                        height: 40
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"
                    Label:
                        size_hint: (1, None)
                        height: 100
                        text: "Country"

            MDBoxLayout:
                AnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    MapWidget:
                        zoom: 4
                        lat: 38.6394
                        lon: -100.057
                
""")


class MapWidget(MapView):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.map_source = MapSource(url=URL, image_ext="png")


class MapScreen(Screen):
    map_source = MapSource(url=URL, image_ext="png")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
