from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

from ui.widgets.label_button import LabelButton


Builder.load_string("""
<CitySelection>
    id: city_box
    orientation: "vertical"
    spacing: dp(5), dp(10)
    height: dp(50)
    BoxLayout:
        orientation: "horizontal"
        padding: dp(5), dp(7)
        Widget:
            size_hint_x: 0.2
        MDFlatButton:
            id: city
            size_hint_x: 0.6
            text: root.city_label
            theme_text_color: "Custom"
            text_color: (1,1,1,1)
            pos_hint: {'center_x': 0, 'center_y': .5}
            on_release: root.connect_to_city()
        Widget:
            size_hint_x: 0.1
    MDSeparator:

<CountrySelection>
    id: country_selection
    height: root.height
    padding: dp(5), dp(7)
    size_hint_y: None
    cols: 1
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            id: country_box
            orientation: "horizontal"
            size_hint_x: 1
            height: dp(50)
            Image:
                source: root.flag
                size_hint_x: 0.2
                height: dp(50)
            MDFlatButton:
                height: dp(50)
                size_hint_x: 0.5
                text: root.country_label
                theme_text_color: "Custom"
                text_color: (1,1,1,1)
                pos_hint: {'center_x': 0, 'center_y': .5}
                on_release: root.connect_to_country()
            MDIconButton:
                id: drop_down
                icon: "chevron-down"
                height: dp(50)
                pos_hint: {'center_x': .5, 'center_y': .5}
                on_release: root.build_drop_down()
        Widget:
            id: padding
            height: dp(5)
        MDSeparator:
            id: separator
            height: dp(1)
            padding: dp(10),0,0,0
""")


class CitySelection(BoxLayout):
    city_label = StringProperty("")
    city = StringProperty("")

    def __init__(self, city, connect, **kwargs):
        super().__init__(**kwargs)
        self.city_label = city
        self.city = city
        self.connect = connect
        self.nord_client = App.get_running_app().nord_client

    def connect_to_city(self):
        print("got here city hit")
        self.connect(self.city)


class CountrySelection(GridLayout):
    country_label = StringProperty("")
    flag = StringProperty("")
    drop_down_icon = StringProperty("chevron-down")

    def __init__(self, country, connect, **kwargs):
        super().__init__(**kwargs)
        self.expanded = False
        self.connect = connect
        self.country = country
        self.country_label = country.replace("_", " ")
        _country = country.replace("_", "-").lower()
        self.flag = f"ui/assets/images/{_country}.png"
        self.nord_client = App.get_running_app().nord_client
        self.cities = self.nord_client.country_dict[country]

    def connect_to_country(self):
        self.connect(self.country)

    def build_drop_down(self, *args):
        if not self.expanded:
            for city in self.cities:
                self.add_widget(CitySelection(city=city, connect=self.connect))
            self.expanded = True
            self._update_height()
        else:
            widgets_to_remove = []
            for widget in self.children:
                if isinstance(widget, CitySelection):
                    widgets_to_remove.append(widget)
            for widget in widgets_to_remove:
                self.remove_widget(widget)
            self.expanded = False
            self.height = dp(56)


    def _update_height(self):
        height = 0
        for child in self.children:
            height += child.height
        self.height = height

