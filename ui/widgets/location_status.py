from kivy.properties import StringProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.label import MDIcon


Builder.load_string("""
<LocationStatus>
    id: location_status
    orientation: "horizontal"
    padding: dp(10), dp(10)
    MDIcon:
        id: world_icon
        icon: "earth"
        size_hint_x: 0.15
        font_size: 40
        theme_text_color: "Hint"
        valign: "center"
    MDLabel:
        size_hint_x: 0.6
        id: location_label
        text: root.location_label
        font_style: "Subtitle1"
        font_size: 28
        valign: "center"
        halign: "center"
    MDLabel:
        id: number_label
        size_hint_x: 0.25
        text: root.location_number
        font_style: "Subtitle1"
        font_size: 28
        valign: "center"
""")


class LocationStatus(BoxLayout):
    location_label = StringProperty("Mexico")
    location_number = StringProperty("#51")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_locaation(self, location, number):
        self.location_label = location
        self.location_number = number
