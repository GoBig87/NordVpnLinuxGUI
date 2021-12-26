from kivy.properties import StringProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.label import MDIcon

from ui.constants import ERROR_COLOR, SUCCESS_COLOR


Builder.load_string("""
<ProtectionStatus>
    id: protection_status
    orientation: "horizontal"
    padding: dp(10), dp(10)
    Widget:
        size_hint_x: 0.1
    BoxLayout:
        orientation: "horizontal"
        MDIcon:
            id: alert_icon
            icon: root.icon
            size_hint_x: 0.3
            font_size: 40
            color: root.protection_color
            valign: "center"
        MDLabel:
            id: alert_label
            text: root.label_text
            font_style: "Subtitle1"
            font_size: 24
            color: root.protection_color
            valign: "center"
""")


class ProtectionStatus(BoxLayout):
    protection_color = ColorProperty(ERROR_COLOR)
    label_text = StringProperty("Unprotected")
    icon = StringProperty("shield-off-outline")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_protected(self):
        self.protection_color = SUCCESS_COLOR
        self.label_text = "Protected"
        self.icon = "shield-link-variant"

    def set_unprotected(self):
        self.protection_color = ERROR_COLOR
        self.label_text = "Unprotected"
        self.icon = "shield-off-outline"