from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy_garden.mapview import MapView, MapSource, MapMarker
from kivy.app import App
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest

from ui.widgets.dialog_spinner import DialogSpinner
from ui.widgets.status_dialog import StatusDialog
from ui.widgets.status_box import StatusBox
from ui.widgets.country_selection import CountrySelection
from ui.widgets.group_selection import GroupSelection
from ui.constants import URL


Builder.load_string("""
<MapScreen>
    BoxLayout:
        orientation: "vertical"
        MDCard:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(80)
            padding: 0, dp(10)
            BoxLayout:
                orientation: "horizontal"
                size_hint_x: 0.2
                Widget:
            StatusBox:
                id: status_box
                size_hint_x: 0.7
            BoxLayout:
                orientation: "vertical"
                padding: dp(10), dp(10)
                size_hint_x: 0.2
                Widget:
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.9
            MDCard:
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
                        id: map
                        zoom: 4
                        lat: 38.6394
                        lon: -100.057
    AnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(20), dp(20)
        MDFillRoundFlatButton:
            text: root.connection
            on_press: root.quick_connect()
    AnchorLayout:
        anchor_x: "left"
        anchor_y: "top"
        padding: dp(10), dp(10)
        MDIconButton:
            icon: "cog"
            on_press: root.switch_screen()  
    AnchorLayout:
        anchor_x: "right"
        anchor_y: "top"
        padding: dp(10), dp(15)
        MDIconButton:
            icon: "information-outline"
            on_press: root.open_status_dialog() 
""")


class MapWidget(MapView):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.map_source = MapSource(url=URL, image_ext="png")
        self.marker = MapMarker(keep_ratio=True,
                                allow_stretch=True,
                                size_hint_y=None,
                                size_hint_x=None,
                                height=50)
        self.marker.source = "ui/assets/images/marker.png"
        self.marker.lat = 38.6394
        self.marker.lat = -100.057
        self.marker.height = 60
        self.marker.width = 40
        self.add_marker(self.marker)

    def on_touch_down(self, touch):
        pass

    def on_touch_up(self, touch):
        pass

    def on_touch_move(self, touch):
        pass


class MapScreen(Screen):
    map_source = MapSource(url=URL, image_ext="png")
    email = StringProperty("")
    country = StringProperty("Disconnected")
    search_text = StringProperty("")
    connection = StringProperty("Log in")

    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        self.nord_client = App.get_running_app().nord_client
        self.ids.status_box.ids.login_status.bind(on_press=self.handle_login)
        self.login_dialog = DialogSpinner(info_text="Logging in..")
        self.status_dialog = StatusDialog()
        self.login_dialog.bind(on_dismiss=self.cancel_login)
        self.connecting_dialog = DialogSpinner(info_text="Connecting..")
        self.ids.status_box.ids.location_status.location_label = self.country
        if self.nord_client.email:
            self.update_login()
        if self.nord_client.status_dict.get("Country"):
            self.update_connected()
        self.build_server_list()
        self.update_gps_location()

    def build_server_list(self, search_text=""):
        self.ids.selection.clear_widgets()
        self.build_specialty_list(search_text)
        self.build_country_list(search_text)

    def build_specialty_list(self, search_text=""):
        label = MDLabel(text="Specialty Servers",
                        size_hint=(1, None),
                        height=dp(50),
                        bold=True,
                        padding=(dp(29), 0),
                        halign="left")
        self.ids.selection.add_widget(label)
        for group in self.nord_client.group_list:
            if search_text:
                if search_text.lower() in group.lower():
                    self.ids.selection.add_widget(GroupSelection(group=group, connect=self.connect))
            else:
                self.ids.selection.add_widget(GroupSelection(group=group, connect=self.connect))

    def build_country_list(self, search_text=""):
        label = MDLabel(text="Location Servers",
                        size_hint=(1, None),
                        height=dp(50),
                        bold=True,
                        padding=(dp(29), 0),
                        halign="left")
        self.ids.selection.add_widget(label)
        for country in self.nord_client.country_dict:
            if search_text:
                if search_text.lower() in country.lower():
                    self.ids.selection.add_widget(CountrySelection(country=country,
                                                                   connect=self.connect))
            else:
                self.ids.selection.add_widget(CountrySelection(country=country,
                                                               connect=self.connect))

    def handle_login(self, *args):
        if self.email:
            self.nord_client.logout(self.logout_success, self.logout_error)
        else:
            self.login_dialog.open()
            self.nord_client.login(self.nord_client.login_success, self.login_fail)
            self.account_check_timer = Clock.schedule_interval(self.account_check, 1)

    def cancel_login(self, *args):
        self.account_check_timer.cancel()

    def logged_in(self, output):
        self.login_button.text = "Logging in..."

    def login_fail(self, output):
        self.login_dialog.info_text = "Login failed"

    def logout_success(self, output):
        # Warning order matters here
        self.nord_client.get_account_info()
        self.nord_client.get_status()
        self.updated_disconnected()
        self.update_logout()

    def logout_error(self, output):
        self.login_dialog.info_text = "Login failed"

    @mainthread
    def update_login(self):
        self.email = self.nord_client.email
        self.ids.status_box.ids.login_status.set_logged_in(self.email)
        self.connection = "Quick Connect"

    @mainthread
    def update_logout(self):
        self.email = ""
        self.ids.status_box.ids.login_status.set_logged_out()
        self.connection = "Log in"

    def account_check(self, dt):
        print("Checking account....")
        if not self.nord_client.logged_in:
            print("not logged in...")
            self.nord_client.get_account_info()
        else:
            self.nord_client.get_account_info()
            self.update_login()
            self.account_check_timer.cancel()
            Clock.schedule_once(self.delay_dismiss, 1.5)

    @mainthread
    def update_connected(self):
        self.country = self.nord_client.status_dict["Country"]
        self.ids.status_box.ids.location_status.location_label = self.country
        self.ids.status_box.ids.protection_status.set_protected()
        self.connection = "Disconnect"

    @mainthread
    def updated_disconnected(self):
        self.country = "Disconnected"
        self.ids.status_box.ids.location_status.location_label = self.country
        self.ids.status_box.ids.protection_status.set_unprotected()
        self.connection = "Quick Connect"

    def connect(self, selection):
        print("callback hit")
        self.connecting_dialog.info_text = "Connecting"
        self.connecting_dialog.open()
        self.nord_client.connect(selection, self.connect_success, self.connect_error)

    def quick_connect(self):
        if self.connection == "Log in":
            self.handle_login()
        elif self.connection == "Quick Connect":
            self.connecting_dialog.info_text = "Connecting"
            self.connecting_dialog.open()
            self.nord_client.quick_connect(self.connect_success, self.connect_error)
        elif self.connection == "Disconnect":
            self.connecting_dialog.info_text = "Disconnecting"
            self.connecting_dialog.open()
            self.nord_client.disconnect(self.disconnect_success, self.disconnect_error)

    def connect_success(self, outs):
        print("connect success")
        self.connecting_dialog.info_text = "Connected"
        self.connection = "Disconnect"
        self.nord_client.get_status()
        self.update_connected()
        self.update_gps_location()
        Clock.schedule_once(self.delay_dismiss, 1.5)

    def connect_error(self, outs):
        print("failed to connect")
        self.connecting_dialog.info_text = "Failed to Connect"
        Clock.schedule_once(self.delay_dismiss, 1.5)

    def disconnect_success(self, outs):
        self.connecting_dialog.info_text = "Disconnected"
        self.connection = "Quick Connect"
        self.nord_client.get_status()
        self.updated_disconnected()
        Clock.schedule_once(self.delay_dismiss, 1.5)

    def disconnect_error(self, outs):
        self.connecting_dialog.info_text = "Failed to Connect"
        Clock.schedule_once(self.delay_dismiss, 1.5)

    @mainthread
    def delay_dismiss(self, dt):
        self.connecting_dialog.dismiss()
        self.login_dialog.dismiss()

    def update_gps_location(self):
        url = 'http://ipinfo.io/json'
        UrlRequest(url,
                   on_success=self.location_success,
                   on_error=self.location_error)

    def location_success(self, req, result):
        loc = result.get("loc")
        lat, lon = loc.replace(" ", "").split(",")
        self.ids.map.marker.lat = float(lat)
        self.ids.map.marker.lon = float(lon)
        self.ids.map.center_on(float(lat), float(lon))

    def location_error(self, req, result):
        pass

    def open_status_dialog(self):
        self.nord_client.get_status(self.open_status_dialog_cb, self.connect_error)

    def open_status_dialog_cb(self, output):
        status_dict = self.nord_client.get_status_resp(output)
        self.status_dialog.update_data(status_dict)

    def switch_screen(self):
        App.get_running_app().content.current = "settings"
