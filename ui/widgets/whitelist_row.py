from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder


Builder.load_string("""
<WhitelistRow>
    id: whitelist
    orientation: "vertical"
    padding: dp(10), dp(10)
    size_hint_y: None
    height: dp(50)
    Widget:
        size_hint_y: 0.05
    BoxLayout
        orientation: "horizontal"
        Widget:
            size_hint_x: 0.05
        MDLabel:
            text: root.whitelist_type
            size_hint_x: 0.3
            font_size: 24
            valign: "center"
        Widget:
        BoxLayout:
            orientation: "horizontal"
            Widget:
                size_hint_x: 0.2
            MDLabel:
                id: subnet
                text: root.subnet_text
                font_style: "Subtitle1"
                font_size: 24
                valign: "center"
            MDFlatButton:
                text: "Remove"
                on_press: root.remove_subnet()
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                pos_hint: {'center_x': .5, 'center_y': .5}
        Widget:
            size_hint_x: 0.05
    Widget:
        size_hint_y: 0.05
    MDSeparator:
        height: dp(1)
""")


class WhitelistRow(BoxLayout):
    subnet_text = StringProperty("")
    whitelist_type = StringProperty("")

    def __init__(self, remove_cb, **kwargs):
        super().__init__(**kwargs)
        self.remove_cb = remove_cb

    def remove_subnet(self, *args):
        self.remove_cb(self.subnet_text)

