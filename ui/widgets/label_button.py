from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel


class LabelButton(MDLabel, ButtonBehavior):
    def __init__(self, **kwargs):
        super(LabelButton, self).__init__(**kwargs)