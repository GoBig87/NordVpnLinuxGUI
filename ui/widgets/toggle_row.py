from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder


Builder.load_string("""
<ToggleRow>
    orientation: "vertical"
    BoxLayout:
        orientation: "horizontal"
        MDLabel:   
            text: root.label
            font_style: root.font_style
            font_size: root.font_size
        Widget:
        MDSwitch:
            id: switch
            name: root.name
            on_press: root.handle_toggle(self)
            pos_hint: {'center_x': .5, 'center_y': .5}
    MDSeparator:
        height: dp(1)
""")


class ToggleRow(BoxLayout):
    label = StringProperty("")
    name = StringProperty("")
    font_style = StringProperty("Caption")
    font_size = NumericProperty("24")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_cb(self, *args):
        # Override in parent
        pass

    def handle_toggle(self, *args):
        self.toggle_cb(self.name)

