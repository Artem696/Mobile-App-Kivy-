from kivy.app import App
from kivy.uix.widget import Widget
 
 
class Pets(Widget):
     pass
 
 
class PetsApp(App):
    def build(self):
        return Pets()


if __name__ == '__main__':
     PetsApp().run()