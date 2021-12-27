from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.app import App
from kivy.clock import mainthread
from kivymd.toast import toast

from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu

from ui.widgets.whitelist_row import WhitelistRow
from ui.widgets.toggle_row import ToggleRow


Builder.load_string("""
<IconListItem>
    IconLeftWidget:
        icon: root.icon
        
<SettingsScreen>
    BoxLayout:
        id: settings
        orientation: "vertical"
        MDCard:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(70)
            padding: 0, dp(10)
            Widget:
            MDLabel:
                text: "Settings"
                font_type: "H4"
                font_size: 30
                bold: True
                halign: "center"
            Widget:
        Widget:
            size_hint_y: None
            height: dp(40)
        
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            MDBoxLayout:
                id: selection
                orientation: "vertical"
                size_hint_y: None
                height: dp(1400)
                BoxLayout:
                    orientation: "horizontal" 
                    Widget:
                        size_hint_x: 0.25          
                    MDCard:
                        orientation: "vertical"
                        padding: dp(20), dp(20)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:
                                size_hint_x: 0.25
                                text: "General"
                                font_style: "H4"
                                font_size: 36
                                bold: True
                            Widget:
                                size_hint_x: 0.75
                        ToggleRow:
                            id: Auto-connect
                            label: "Auto-Connect"
                            name: "autoconnect"
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Set custom DNS"
                                font_style: "Caption"
                                font_size: 24
                            Widget:
                            MDTextField:
                                id: DNS
                                name: "DNS"
                                hint_text: 'DNS Server'
                                pos_hint: {'center_x': .5, 'center_y': .5}
                            Widget:
                                size_hint_x: 0.05
                            MDFlatButton:
                                text: "Set DNS"
                                on_release: root.set_dns()
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:
                            height: dp(1)
                        ToggleRow:
                            id: Firewall
                            label: "Firewall"
                            name: "firewall"
                        ToggleRow:
                            id: Kill_Switch
                            label: "Kill Switch"
                            name: "killswitch"
                        ToggleRow:
                            id: Notify
                            label: "Notifications"
                            name: "notify"
                        ToggleRow:
                            id: CyberSec
                            label: "CyberSec"
                            name: "cybersec"    
                        ToggleRow:
                            id: IPv6
                            label: "IPv6"
                            name: "ipv6"               
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:
                                size_hint_x: 0.25
                                text: "Protocol"
                                font_style: "Caption"
                                font_size: 24
                            Widget:
                            MDDropDownItem:
                                id: Protocol
                                name: "Protocol"
                                pos_hint: {'center_x': .5, 'center_y': .5}
                                text: 'TCP/UDP'
                                on_release: root.protocol.open()     
                        MDSeparator:
                            height: dp(1)              
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:
                                size_hint_x: 0.25
                                text: "Technology"
                                font_style: "Caption"
                                font_size: 24
                            Widget:
                            MDDropDownItem:
                                id: Technology
                                name: "Technology"
                                pos_hint: {'center_x': .5, 'center_y': .5}
                                text: 'Technology'
                                on_release: root.technology.open()
                        MDSeparator:
                            height: dp(1)  
                        Widget:
                            size_hint_y: None
                            height: dp(20)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:
                                size_hint_x: 0.5
                                text: "Whitelist"
                                font_style: "H4"
                                font_size: 36
                                bold: True
                            Widget:
                                size_hint_x: 0.5    
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Set Subnet"
                                font_style: "Caption"
                                font_size: 24
                            Widget:
                            MDTextField:
                                id: add_subnet
                                hint_text: 'Subnet'
                                pos_hint: {'center_x': .5, 'center_y': .5}
                            Widget:
                                size_hint_x: 0.05
                            MDFlatButton:
                                text: "Whitelist"
                                on_release: root.add_whitelist_subnet(self)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:       
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Set Port"
                                font_style: "Caption"
                                font_size: 24
                            Widget:
                            MDTextField:
                                id: add_port
                                hint_text: 'Port'
                                pos_hint: {'center_x': .5, 'center_y': .5}
                            Widget:
                                size_hint_x: 0.05
                            MDFlatButton:
                                text: "Whitelist"
                                on_release: root.add_whitelist_port(self)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:       
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:
                                size_hint_x: 0.5
                                text: "Active Whitelist"
                                font_style: "H4"
                                font_size: 28
                                bold: True
                            Widget:
                                size_hint_x: 0.5  
                        GridLayout:    
                            id: Whitelisted_subnets
                            name: "Whitelisted_subnets"  
                            height: self.height
                            padding: dp(5), dp(7)
                            size_hint_y: None
                            cols: 1  
                        GridLayout:
                            id: Whitelisted_ports
                            name: "Whitelisted_ports" 
                            height: self.height
                            padding: dp(5), dp(7)
                            size_hint_y: None
                            cols: 1         
                    Widget:
                        size_hint_x: 0.25                  
        Widget:
            size_hint_y: 0.1
    AnchorLayout:
        anchor_x: "left"
        anchor_y: "top"
        padding: dp(10), dp(10)
        MDIconButton:
            icon: "arrow-left"
            on_press: root.switch_screen()         
 """)


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.nord_client = App.get_running_app().nord_client
        self.ids["Auto-connect"].handle_toggle = self.handle_toggle
        self.ids["Firewall"].handle_toggle = self.handle_toggle
        self.ids["Kill_Switch"].handle_toggle = self.handle_toggle
        self.ids["Notify"].handle_toggle = self.handle_toggle
        self.ids["CyberSec"].handle_toggle = self.handle_toggle
        self.ids["IPv6"].handle_toggle = self.handle_toggle

        # Drop down menu
        item_nord_lynx = {
            "viewclass": "IconListItem",
            "icon": "access-point-network",
            "text": "NordLynx",
            "height": dp(56),
            "on_release": self.set_technology_nordlynx,
        }
        item_open_vpn = {
            "viewclass": "IconListItem",
            "icon": "access-point-network",
            "text": "OpenVPN",
            "height": dp(56),
            "on_release": self.set_technology_openvpn,
        }
        item_tcp = {
            "viewclass": "IconListItem",
            "icon": "access-point-network",
            "text": "TCP",
            "height": dp(56),
            "on_release": self.set_protocol_tcp,
        }
        item_udp = {
            "viewclass": "IconListItem",
            "icon": "access-point-network",
            "text": "UDP",
            "height": dp(56),
            "on_release": self.set_protocol_udp,
        }
        protocol_items = [
            item_tcp,
            item_udp
        ]
        technology_items = [
            item_open_vpn,
            item_nord_lynx
        ]
        self.protocol = MDDropdownMenu(
            caller=self.ids.Protocol,
            items=protocol_items,
            position="center",
            width_mult=4,
        )
        self.protocol.bind()
        self.technology = MDDropdownMenu(
            caller=self.ids.Technology,
            items=technology_items,
            position="center",
            width_mult=4,
        )
        self.technology.bind()
        self.update_settings()

    def handle_toggle(self, switch):
        setting = switch.name.lower()
        if not switch.active:
            self.nord_client.set_setting_enabled(setting,
                                                 self.success_cb,
                                                 self.error_cb
                                                 )
        else:
            self.nord_client.set_setting_disabled(setting,
                                                  self.success_cb,
                                                  self.error_cb
                                                  )

    def set_protocol_udp(self, *args):
        self.ids.Protocol.text = "UDP"
        self.nord_client.set_protocol("UDP", self.success_cb, self.error_cb)
        self.protocol.dismiss()

    def set_protocol_tcp(self, *args):
        self.ids.Protocol.text = "TCP"
        self.nord_client.set_protocol("TCP", self.success_cb, self.error_cb)
        self.protocol.dismiss()

    def set_technology_openvpn(self, *args):
        self.ids.Technology.text = "OpenVPN"
        self.nord_client.set_technology("OpenVPN", self.success_cb, self.error_cb)
        self.technology.dismiss()

    def set_technology_nordlynx(self, *args):
        self.ids.Technology.text = "NordLynx"
        self.nord_client.set_technology("NordLynx", self.success_cb, self.error_cb)
        self.technology.dismiss()

    def success_cb(self, output):
        self.nord_client.get_settings(self.update_settings_cb, self.error_cb)

    @mainthread
    def error_cb(self, output):
        toast(f"Error: {output}")

    @mainthread
    def update_settings_cb(self, outputs):
        self.nord_client.get_settings_resp(outputs)
        self.update_settings()

    def update_settings(self):
        settings = self.nord_client.settings_dict
        for setting, value in settings.items():
            ids = setting
            ids.replace(" ", "_")
            widget = self.ids[ids]
            if setting in ["DNS", "Protocol", "Technology"]:
                self.ids[setting].text = value
            elif setting == "Whitelisted_subnets":
                self.update_white_list(setting, value, "Subnet:")
            elif setting == "Whitelisted_ports":
                self.update_white_list(setting, value, "Port:")
            elif value == "enabled":
                widget.ids.switch.active = True
            elif value == "disabled":
                widget.ids.switch.active = False

    def update_white_list(self, setting, value, type):
        self.ids[setting].clear_widgets()
        if "Port" in type:
            remove_cb = self.remove_whitelist_port
        else:
            remove_cb = self.remove_whitelist_subnet
        for whitelist in value:
            self.ids[setting].add_widget(WhitelistRow(subnet_text=whitelist,
                                                      whitelist_type=type,
                                                      remove_cb=remove_cb,
                                                      ))
        self._update_height(self.ids[setting])

    def set_dns(self, *args):
        dns = self.ids.DNS.text
        self.nord_client.set_dns(dns, self.success_cb, self.error_cb)
        self.ids.DNS.text = ""

    def add_whitelist_port(self, *args):
        port = self.ids.add_port.text
        self.nord_client.add_whitelist_port(port, self.success_cb, self.error_cb)
        self.ids.add_port.text = ""

    def add_whitelist_subnet(self, *args):
        subnet = self.ids.add_subnet.text
        if "/" not in subnet:
            subnet = subnet + "/24"
        self.nord_client.add_whitelist_subnet(subnet, self.success_cb, self.error_cb)
        self.ids.add_subnet.text = ""

    def remove_all_whitelist(self, *args):
        self.nord_client.remove_all_whitelist(self.success_cb, self.error_cb)

    def remove_all_whitelist_port(self, *args):
        self.nord_client.remove_all_whitelist_port(self.success_cb, self.error_cb)

    def remove_all_whitelist_subnet(self, *args):
        self.nord_client.remove_all_whitelist_subnet(self.success_cb, self.error_cb)

    def remove_whitelist_port(self, port):
        port = port.replace("(UDP|TCP)", "")
        self.nord_client.remove_whitelist_port(port, self.success_cb, self.error_cb)

    def remove_whitelist_subnet(self, subnet):
        self.nord_client.remove_whitelist_subnet(subnet, self.success_cb, self.error_cb)

    def switch_screen(self):
        App.get_running_app().content.current = "map"

    def _update_height(self, parent):
        height = 0
        for child in parent.children:
            height = height + child.height
        parent.height = height

