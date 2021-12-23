from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout

from ui.widgets.label_button import LabelButton


Builder.load_string("""
<CitySelection>
    id: city_box
    orientation: "vertical"
    spacing: dp(5), dp(20)
    height: 80
    BoxLayout:
        orientation: "horizontal"
        padding: dp(5), dp(7)
        Widget:
            size_hint_x: 0.2
        LabelButton:
            id: city
            size_hint_x: 0.6
            text: root.city_label
            font_style: "Subtitle1"
            font_size: 24
            valign: "center"
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
        id: country_box
        orientation: "horizontal"
        size_hint_x: 1
        height: 70
        Image:
            source: root.flag
            size_hint_x: 0.2
        Widget:
            size_hint_x: 0.1
        LabelButton:
            size_hint_x: 0.6
            text: root.country_label
            font_style: "Subtitle1"
            font_size: 24
            valign: "center"
            on_release: root.connect_to_country()
        MDIconButton:
            id: drop_down
            icon: "chevron-down"
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: root.build_drop_down()
    Widget:
        id: padding
        height: 5
    MDSeparator:
        id: separator
        height: 5
        padding: dp(10),0,0,0
""")


class CitySelection(BoxLayout):
    city_label = StringProperty("")
    city = StringProperty("")

    def __init__(self, city, **kwargs):
        super().__init__(**kwargs)
        self.city_label = city
        self.city = city
        self.nord_client = App.get_running_app().nord_client

    def connect_to_city(self):
        self.nord_client.connect_to_city(self.city)

class CountrySelection(GridLayout):
    country_label = StringProperty("")
    flag = StringProperty("")
    drop_down_icon = StringProperty("chevron-down")

    def __init__(self, country, **kwargs):
        super().__init__(**kwargs)
        self.expanded = False
        self.country = country
        self.country_label = country.replace("_", "")
        _country = country.replace("_", "-").lower()
        self.flag = f"ui/assets/images/{_country}.png"
        self.nord_client = App.get_running_app().nord_client
        self.cities = self.nord_client.country_dict[country]

    def connect_to_country(self):
        self.nord_client.connect_to_country(self.country)

    def build_drop_down(self, *args):
        if not self.expanded:
            for city in self.cities:
                self.add_widget(CitySelection(city=city))
            self.expanded = True
        else:
            widgets_to_remove = []
            for widget in self.children:
                if isinstance(widget, CitySelection):
                    widgets_to_remove.append(widget)
            for widget in widgets_to_remove:
                self.remove_widget(widget)
            self.expanded = False
        self._update_height()

    def _update_height(self):
        height = 0
        for child in self.children:
            height += child.height
        self.height = height
