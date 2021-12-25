from kivy.properties import StringProperty, NumericProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import BaseDialog
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp


Builder.load_string("""
<DialogContainer@MDCard+FakeRectangularElevationBehavior>

<DialogSpinner>
    DialogContainer:
        id: container
        orientation: "horizontal"
        size_hint_y: None
        height: self.minimum_height
        elevation: 24
        height: dp(50)
        width: dp(200)
        padding: "12dp", "12dp", "8dp", "8dp"
        radius: root.radius
        md_bg_color:
            root.theme_cls.bg_dark \
            if not root.md_bg_color else root.md_bg_color
        MDSpinner:
            size_hint: None, None
            size: dp(30), dp(30)
            active: True
            valign: "center"
        Widget:
            size_hint_x: 0.1
        MDLabel:
            text: root.info_text
            font_style: "H6"
            font_size: 30
            valign: "center"
        Widget:
            size_hint_x: 0.1
            
""")

class DialogSpinner(BaseDialog):
    info_text = StringProperty("Signing in...")
    width_offset = NumericProperty(dp(48))
    md_bg_color = ColorProperty(None)
    _scroll_height = NumericProperty("28dp")
    _spacer_top = NumericProperty("24dp")

    def __init__(self, **kwargs):
        super(DialogSpinner, self).__init__(**kwargs)
        super().__init__(**kwargs)
        Window.bind(on_resize=self.update_width)

        self.size_hint = (None, None)
        self.width = dp(250)

        update_height = False
        if update_height:
            Clock.schedule_once(self.update_height)

    def update_width(self, *args):
        self.width = dp(250)

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