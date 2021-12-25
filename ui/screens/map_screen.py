from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy_garden.mapview import MapView, MapSource
from kivy.app import App
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from ui.widgets.dialog_spinner import DialogSpinner
from ui.widgets.status_box import StatusBox
from ui.widgets.country_selection import CountrySelection
from ui.widgets.group_selection import GroupSelection
from ui.constants import URL

Builder.load_string("""
<MapScreen>
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            padding: 0, dp(10)
            BoxLayout:
                orientation: "horizontal"
                size_hint_x: 0.2
                Widget:
            StatusBox:
                id: status_box
                size_hint_x: 0.6
            BoxLayout:
                orientation: "vertical"
                padding: dp(10), dp(10)
                size_hint_x: 0.2
                MDLabel:
                    text: root.email
                    font_style: "Subtitle1"
                    font_size: 18
                    bold: True
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.9
            BoxLayout:
                orientation: "vertical"
                size_hint_x: 0.4
                MDBoxLayout:
                    padding: dp(10), dp(10)
                    adaptive_height: True
                    MDIconButton:
                        icon: 'magnify'
                    MDTextField:
                        id: search_field
                        hint_text: 'Search Server'
                        on_text: root.build_server_list(self.text)
                ScrollView:
                    do_scroll_x: False
                    do_scroll_y: True
                    MDBoxLayout:
                        id: selection
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
            BoxLayout:
                AnchorLayout:
                    anchor_x: "center"
                    anchor_y: "center"
                    MapWidget:
                        zoom: 4
                        lat: 38.6394
                        lon: -100.057
    AnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(20), dp(20)
        MDFillRoundFlatButton:
            text: "Quick Connect"
    AnchorLayout:
        anchor_x: "left"
        anchor_y: "top"
        padding: dp(5), dp(5)
        MDIconButton:
            icon: "cog"     
""")


class MapWidget(MapView):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.map_source = MapSource(url=URL, image_ext="png")


class MapScreen(Screen):
    map_source = MapSource(url=URL, image_ext="png")
    email = StringProperty("")
    search_text = StringProperty("")

    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        self.nord_client = App.get_running_app().nord_client
        self.ids.status_box.ids.login_status.ids.login_label.bind(on_press=self.handle_login)
        self.build_server_list()
        self.login_dialog = DialogSpinner(info_text="Logging in..")
        self.login_dialog.bind(on_dismiss=self.cancel_login)
        self.connecting_dialog = DialogSpinner(info_text="Connecting..")

    def build_server_list(self, search_text=""):
        self.ids.selection.clear_widgets()
        self.build_specialty_list(search_text)
        self.build_country_list(search_text)

    def build_specialty_list(self, search_text=""):
        label = MDLabel(text="Specialty List", size_hint=(1, None), height=dp(50), bold=True, halign="center")
        self.ids.selection.add_widget(label)
        for group in self.nord_client.group_list:
            if search_text:
                if search_text in group:
                    self.ids.selection.add_widget(GroupSelection(group=group))
            else:
                self.ids.selection.add_widget(GroupSelection(group=group))

    def build_country_list(self, search_text=""):
        label = MDLabel(text="Country List", size_hint=(1, None), height=dp(50), bold=True, halign="center")
        self.ids.selection.add_widget(label)
        for country in self.nord_client.country_dict:
            if search_text:
                if search_text in country:
                    self.ids.selection.add_widget(CountrySelection(country=country))
            else:
                self.ids.selection.add_widget(CountrySelection(country=country))

    def handle_login(self, instance):
        self.login_dialog.open()
        self.nord_client.login(self.nord_client.login_success, self.login_fail)
        self.account_check_timer = Clock.schedule_interval(self.account_check, 1)

    def cancel_login(self):
        self.account_check_timer.cancel()
        self.login_dialog.dismiss()

    def logged_in(self, output):
        self.login_button.text = "Logging in..."

    def login_fail(self, output):
        self.login_dialog.info_text = "Login failed"

    def account_check(self, dt):
        print("Checking account....")
        if not self.nord_client.logged_in:
            print("not logged in...")
            self.nord_client.account(self.nord_client.check_login, self.login_fail)
        else:
            self.ids.status_box.ids.login_status.login_text = "Logged In"
            self.ids.status_box.ids.login_status.login_icon = "logout"
            self.email = self.nord_client.email
            self.cancel_login()
