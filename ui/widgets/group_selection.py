from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout

from ui.widgets.label_button import LabelButton


Builder.load_string("""
<GroupSelection>
    id: country_selection
    height: root.height
    padding: dp(5), dp(7)
    size_hint_y: None
    cols: 1
    BoxLayout:
        id: country_box
        orientation: "horizontal"
        size_hint_x: 1
        height: 70
        MDIcon:
            icon: root.group_icon
            size_hint_x: 0.2
        Widget:
            size_hint_x: 0.1
        LabelButton:
            size_hint_x: 0.6
            text: root.group_label
            font_style: "Subtitle1"
            font_size: 24
            valign: "center"
            on_release: root.connect_to_group()
        Widget:
    Widget:
        id: padding
        height: 5
    MDSeparator:
        id: separator
        height: 5
        padding: dp(10),0,0,0
""")


class GroupSelection(GridLayout):
    group_label = StringProperty("")
    group_icon = StringProperty("chevron-down")

    def __init__(self, group, **kwargs):
        super().__init__(**kwargs)
        self.group = group
        self.group_label = group.replace("_", " ")
        self.nord_client = App.get_running_app().nord_client

    def connect_to_group(self):
        self.nord_client.connect_to_country(self.country)

