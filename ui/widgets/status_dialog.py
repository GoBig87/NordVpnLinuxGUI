from kivy.properties import StringProperty, NumericProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import BaseDialog
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp

Builder.load_string("""
<DialogContainer@MDCard+FakeRectangularElevationBehavior>

<StatusDialog>
    DialogContainer:
        id: container
        orientation: "vertical"
        size_hint_y: None
        height: self.minimum_height
        elevation: 24
        height: dp(325)
        width: dp(325)
        padding: "12dp", "12dp", "8dp", "8dp"
        radius: root.radius
""")


# Status: Connected
# Current server: mx57.nordvpn.com
# Country: Mexico
# City: Mexico
# Server IP: 192.154.196.27
# Current technology: OPENVPN
# Current protocol: UDP
# Transfer: 49.49 MiB received, 32.15 MiB sent
# Uptime: 10 hours 9 minutes


class StatusDialog(BaseDialog):
    def __init__(self, **kwargs):
        super(StatusDialog, self).__init__(**kwargs)
        super().__init__(**kwargs)
        Window.bind(on_resize=self.update_width)

        self.size_hint = (None, None)
        self.width = dp(325)

        update_height = False
        if update_height:
            Clock.schedule_once(self.update_height)

    def update_width(self, *args):
        self.width = dp(325)

    def update_height(self, *args):
        self._spacer_top = self.content_cls.height + dp(24)

    def on_open(self):
        # TODO: Add scrolling text.
        self.height = self.ids.container.height

    def get_normal_height(self):
        return (
                (Window.height * 80 / 100)
                - self._spacer_top
                - dp(52)
                - self.ids.container.padding[1]
                - self.ids.container.padding[-1]
                - 100
        )

    def update_data(self, status_dict):
        self.ids.container.clear_widgets()
        status = "Status: " + status_dict.get("Status", None)
        current_server = "Current server: " + status_dict.get("Current_server", None)
        country = "Country: " + status_dict.get("Country", None)
        city = "City: " + status_dict.get("City", None)
        server_ip = "Server IP: " + status_dict.get("Server_IP", None)
        technology = "Current technology: " + status_dict.get("Current_technology", None)
        protocol = "Current protocol:" + status_dict.get("Current_protocol", None)
        transfer = "Transfer:" + status_dict.get("Transfer", None)
        uptime = "Uptime:" + status_dict.get("Uptime", None)
        status_array = [
            status,
            current_server,
            country,
            city,
            server_ip,
            technology,
            protocol,
            transfer,
            uptime,
        ]
        for status in status_array:
            self.ids.container.add_widget(MDLabel(
                text=status,
                font_style="Caption",
                font_size=24,
            ))
        self.open()
