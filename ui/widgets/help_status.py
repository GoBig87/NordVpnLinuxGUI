from kivy.properties import StringProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.label import MDIcon

from ui.constants import ERROR_COLOR, SUCCESS_COLOR


Builder.load_string("""
<HelpStatus>
    id: help_status
    orientation: "horizontal"
    padding: dp(10), dp(10)
    MDIcon:
        id: help_icon
        icon: "help"
        size_hint_x: 0.3
        font_size: 40
        theme_text_color: "Custom"
        valign: "center"
    MDLabel:
        id: alert_label
        text: root.the
        font_style: "Subtitle1"
        font_size: 24
        theme_text_color: "Custom"

        valign: "center"
""")


class HelpStatus(BoxLayout):
    protection_color = ColorProperty()
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