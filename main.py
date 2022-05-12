import kivy
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
import requests


# Config.set('graphics', 'width', '414')
# Config.set('graphics', 'height', '736')
# Config.write()

class StartScreen(Screen):
     pass
class MainScreen(Screen):
     pass
class LoginScreen(Screen):
     pass
class Notification_NoReg(Screen):
     pass
class Profile_NoReg(Screen):
     pass
class Lost_Filter(Screen):
     pass
class Ad_Screen(Screen):
     pass
class WindowManager(ScreenManager):
     pass


class Lost_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Tab(MDFloatLayout, MDTabsBase):
     pass
class Lost_list(Tab):
     pass
class Lost_map(Tab):
     pass
class Sign_in(Tab):
     def get_text_sign(self):
          email = self.ids.email_sign.text
          password = self.ids.passw_sign.text
          print(email,password)
class Registration(Tab):
     def get_text_reg():
          pass
class PopupMarker(Widget):
     pass
class NavigationBar(FakeRectangularElevationBehavior,MDFloatLayout):
     pass

 
class PetsApp(MDApp):
     def check_internet(self):
          try:
               request = requests.get('https://www.google.com/', timeout=10)
               return True
          except (requests.ConnectionError, requests.Timeout) as exception:
               self.dialog = MDDialog(title='Ошибка',
                                   text='Отсутствует подключение к Интернету', size_hint=(0.5, 0.2),
                                   buttons=[MDFlatButton(text='ОК', on_release=self.close_dialog)]
                                   )
               self.dialog.open()
     def close_dialog(self,obj):
          self.get_running_app().stop()
     def change_color(self,instance):
          screen = self.root.current
          if instance in self.root.get_screen(screen).ids.values():
               current_id = list(self.root.get_screen(screen).ids.keys())[list(self.root.get_screen(screen).ids.values()).index(instance)]
               if 'nav_icon1' == current_id:
                    for i in range(5):
                         if f'nav_icon{i+1}' == current_id:
                              self.root.get_screen('main').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('main').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
               if 'nav_icon4' == current_id:
                    for i in range(5):
                         if f'nav_icon{i+1}' == current_id:
                              self.root.get_screen('notif_noreg').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('notif_noreg').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
               if 'nav_icon5' == current_id:
                    for i in range(5):
                         if f'nav_icon{i+1}' == current_id:
                              self.root.get_screen('profile_noreg').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('profile_noreg').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1

     def transition_notif(self):
          log_in_user = False
          if log_in_user == False:
               #self.root.transition = NoTransition()
               self.root.current = 'notif_noreg'
     def transition_profile(self):
          log_in_user = False
          if log_in_user == False:
               #self.root.transition = NoTransition()
               self.root.current = 'profile_noreg'
     def add_cards_ads(self):
          for i in range(10):
               card = Lost_card()
               card.bind(on_press=self.display_ad)
               self.root.ids.mainscreen.ids.lost_list.ids.container.add_widget(card)
     def display_ad(self, *args, **kwargs):
          self.root.current = 'ad'
     def on_start(self, **kwargs):
          self.check_internet()
          self.add_cards_ads()
#kv = Builder.load_file("pets.kv")
if __name__ == '__main__':
     PetsApp().run()