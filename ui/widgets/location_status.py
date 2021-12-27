from kivy.properties import StringProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.label import MDIcon


Builder.load_string("""
<LocationStatus>
    id: location_status
    orientation: "horizontal"
    padding: dp(10), dp(10)
    Widget:
        size_hint_x: 0.1
    BoxLayout:
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
            font_size: 24
            valign: "center"
            halign: "center"
    Widget:
        size_hint_x: 0.1
""")


class LocationStatus(BoxLayout):
    location_label = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
