from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.app import App


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
            height: dp(60)
            padding: 0, dp(10)
            BoxLayout:
                orientation: "horizontal"
                size_hint_x: 0.2
                Widget:
            MDLabel:
                text: "Settings"
            BoxLayout:
                orientation: "vertical"
                padding: dp(10), dp(10)
                size_hint_x: 0.2
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
                                font_size: 54
                                bold: True
                            Widget:
                                size_hint_x: 0.75
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Auto Connect"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDSwitch:
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Sets custom DNS"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDTextField:
                                id: dns_field
                                hint_text: 'DNS Server'
                                on_text: root.set_dns(self.text)
                                pos_hint: {'center_x': .5, 'center_y': .5}
                            Widget:
                                size_hint_x: 0.05
                            MDRaisedButton:
                                text: "Set DNS"
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Firewall"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDSwitch:
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                size_hint_x: 0.25
                                text: "Kill Switch"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDSwitch:
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                size_hint_x: 0.25
                                text: "Notifications"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDSwitch:
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                size_hint_x: 0.25
                                text: "Obfuscate"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDSwitch:
                                pos_hint: {'center_x': .5, 'center_y': .5}   
                        MDSeparator:
                            height: dp(1)  
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                size_hint_x: 0.25
                                text: "IPv6"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDSwitch:
                                pos_hint: {'center_x': .5, 'center_y': .5}   
                        MDSeparator:
                            height: dp(1)              
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:
                                size_hint_x: 0.25
                                text: "VPN Protocol"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDDropDownItem:
                                id: drop_item
                                pos_hint: {'center_x': .5, 'center_y': .5}
                                text: 'OpenVPN (TCP)'
                                on_release: root.menu.open()     
                        MDSeparator:
                            height: dp(1)              
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:
                                size_hint_x: 0.25
                                text: "Technology"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDDropDownItem:
                                id: drop_item
                                pos_hint: {'center_x': .5, 'center_y': .5}
                                text: 'Technology'
                                on_release: root.menu.open()
                        MDSeparator:
                            height: dp(1)  
                        Widget:
                            size_hint_y: None
                            height: dp(20)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:
                                size_hint_x: 0.25
                                text: "Whitelist"
                                font_style: "H4"
                                font_size: 54
                                bold: True
                            Widget:
                                size_hint_x: 0.75    
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Set IP to whitelist"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDTextField:
                                id: ip_field
                                hint_text: 'IP Address'
                                on_text: root.whitelist_ip(self.text)
                                pos_hint: {'center_x': .5, 'center_y': .5}
                            Widget:
                                size_hint_x: 0.05
                            MDRaisedButton:
                                text: "Whitelist"
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:       
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Remove IP from whitelist"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDTextField:
                                id: port_field
                                hint_text: 'IP Address'
                                on_text: root.whitelist_ip(self.text)
                                pos_hint: {'center_x': .5, 'center_y': .5}
                            Widget:
                                size_hint_x: 0.05
                            MDRaisedButton:
                                text: "Remove"
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:       
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Remove All IP from whitelist"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            Widget:
                            Widget:
                                size_hint_x: 0.05
                            MDRaisedButton:
                                text: "Remove All"
                                pos_hint: {'center_x': .5, 'center_y': .5}    
                        MDSeparator:
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Set Port to whitelist"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDTextField:
                                id: port_field
                                hint_text: 'Port'
                                on_text: root.whitelist_ip(self.text)
                                pos_hint: {'center_x': .5, 'center_y': .5}
                            Widget:
                                size_hint_x: 0.05
                            MDRaisedButton:
                                text: "Whitelist"
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Remove Port from whitelist"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            MDTextField:
                                id: port_field
                                hint_text: 'Port'
                                on_text: root.whitelist_ip(self.text)
                                pos_hint: {'center_x': .5, 'center_y': .5}
                            Widget:
                                size_hint_x: 0.05
                            MDRaisedButton:
                                text: "Remove"
                                pos_hint: {'center_x': .5, 'center_y': .5}
                        MDSeparator:       
                            height: dp(1)
                        BoxLayout:
                            orientation: "horizontal"
                            MDLabel:   
                                text: "Clear whitelist"
                                font_style: "Caption"
                                font_size: 30
                                bold: True
                            Widget:
                            Widget:
                            Widget:
                                size_hint_x: 0.05
                            MDRaisedButton:
                                text: "Clear All"
                                pos_hint: {'center_x': .5, 'center_y': .5}                            
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
        # Drop down menu
        item_recommended = {
            "viewclass": "IconListItem",
            "icon": "settings-suggest",
            "text": "Suggested Settings",
            "height": dp(56),
            "on_release": self.set_item("Suggested Settings"),
        }
        item_nord_lynx = {
            "viewclass": "IconListItem",
            "icon": "data-usage",
            "text": "NordLynx",
            "height": dp(56),
            "on_release": self.set_item("NordLynx"),
        }
        item_ikev2 = {
            "viewclass": "IconListItem",
            "icon": "shield",
            "text": "IKEv2",
            "height": dp(56),
            "on_release": self.set_item("IKEv2"),
        }
        item_openvpn_tcp = {
            "viewclass": "IconListItem",
            "icon": "access-point-network",
            "text": "OpenVPN (TCP)",
            "height": dp(56),
            "on_release": self.set_item("OpenVPN (TCP)"),
        }
        item_openvpn_udp = {
            "viewclass": "IconListItem",
            "icon": "access-point-network",
            "text": "OpenVPN (UDP)",
            "height": dp(56),
            "on_release": self.set_item("OpenVPN (UDP)"),
        }
        menu_items = [
            item_recommended,
            item_nord_lynx,
            item_ikev2,
            item_openvpn_tcp,
            item_openvpn_udp
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.ids.drop_item.set_item(text_item)
        try:
            self.menu.dismiss()
        except:
            pass

    def set_dns(self, text):
        pass

    def whitelist_ip(self, text):
        pass

    def switch_screen(self):
        App.get_running_app().content.current = "map"
