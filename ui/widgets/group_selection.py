from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout


Builder.load_string("""
<GroupSelection>
    id: country_selection
    height: dp(60)
    padding: dp(5), dp(7)
    size_hint_y: None
    cols: 1
    BoxLayout:
        id: country_box
        orientation: "horizontal"
        MDIcon:
            icon: root.group_icon
            size_hint_x: 0.2
        BoxLayout:
            orientation: "horizontal"
            Widget:
            MDFlatButton:
                text: root.group_label
                theme_text_color: "Custom"
                text_color: (1,1,1,1)
                pos_hint: {'center_x': 0, 'center_y': .5}
                on_release: root.connect_to_group()
            Widget:
    Widget:
        id: padding
        height: dp(5)
    MDSeparator:
        id: separator
        height: dp(1)
        padding: dp(10),0,0,0
""")


class GroupSelection(GridLayout):
    group_label = StringProperty("")
    group_icon = StringProperty("chevron-down")

    def __init__(self, group, connect, **kwargs):
        super().__init__(**kwargs)
        self.group = group
        self.connect = connect
        self.group_label = group.replace("_", " ")
        self.nord_client = App.get_running_app().nord_client

    def connect_to_group(self):
        self.connect(self.group)
