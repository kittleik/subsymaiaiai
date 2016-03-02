import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import ListProperty

#kivy Config
from kivy.config import Config
Config.set('graphics', 'height','1000')
Config.set('graphics', 'width','1200')

class Agent(Widget):

    def __init__(self, **kwargs):
        super(Agent, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0,1,0)
            Rectangle(size=(100,100),
                        pos=self.pos)


class FlatLand(Widget):

    itemIndex = [[0]*10]*10

    def __init__(self, **kwargs):
        super(FlatLand, self).__init__(**kwargs)

        with self.canvas.before:
            Rectangle(source='img/flatland.png',size=(1000, 1000))

        agent = Agent()

        self.add_widget(agent)

        agent.moveUp()

class ControlPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(ControlPanel, self).__init__(**kwargs)
        btn1 = Button(text="^")

        self.add_widget(btn1)
        self.add_widget(Button(text="v"))
        self.add_widget(Button(text=">"))
        self.add_widget(Button(text="<"))

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.add_widget(FlatLand())
        self.add_widget(ControlPanel(orientation='vertical',
                                        size_hint=(.2,1)))


class GUI(App):
    def build(self):
        return RootWidget()
