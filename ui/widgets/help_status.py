from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder


Builder.load_string("""
<HelpStatus>
    id: help_status
    orientation: "horizontal"
    padding: dp(10), dp(10)
    MDIcon:
        id: help_icon
        icon: "help-circle-outline"
        size_hint_x: 0.3
        font_size: 40
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        valign: "center"
    MDLabel:
        id: help_label
        text: "Help"
        font_style: "Subtitle1"
        font_size: 28
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        valign: "center"
""")


class HelpStatus(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
