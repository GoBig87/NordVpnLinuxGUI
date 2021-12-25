from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel


class LabelButton(ButtonBehavior, MDLabel):
    def __init__(self, **kwargs):
        super(LabelButton, self).__init__(**kwargs)