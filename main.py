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
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
import mysql.connector
from mysql.connector import Error
import requests
import re
import hashlib
import os


# Config.set('graphics', 'width', '414')
# Config.set('graphics', 'height', '736')
# Config.write()
current_user = None
def query(query,type):
          try:
               with mysql.connector.connect(
                    host="127.0.0.1",
                    user=("root"),
                    password=("DcA4~6gfec7K"),
                    database="pets"
               ) as connection:
                    if type == "select":
                         with connection.cursor() as cursor:
                              cursor.execute(query)
                              result = cursor.fetchone()[0]
                              return result
                    else:
                         with connection.cursor(buffered=True) as cursor:
                              result = cursor.execute(query)
                              connection.commit()
          except Error as e:
               print(f"The error '{e}' occurred")
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
class Service_List_Screen(Screen):
     pass
class Service_Screen(Screen):
     pass
class Profile_Screen(Screen):
     pass
class Add_Screen(Screen):
     pass
class Add_See_Screen(Screen):
     pass
class Add_Lost_Screen(Screen):
     pass
class Add_Overexposure_Screen(Screen):
     pass
class Add_Nanny_Screen(Screen):
     pass
class Add_Walk_Screen(Screen):
     pass
class Personal_Data(Screen):
     change = StringProperty('Изменить пароль')
class Change_Password_Screen(Screen):
     change = StringProperty('Изменить')
class WindowManager(ScreenManager):
     pass


class Lost_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Service_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Add_see_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Add_lost_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Add_overexposure_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Add_nanny_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Add_walk_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Tab(MDFloatLayout, MDTabsBase):
     pass
class Lost_list(Tab):
     pass
class Lost_map(Tab):
     pass
class Sign_in(Tab):
     def show_dialog(self,text):
          self.dialog = MDDialog(title='Ошибка',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='ОК',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self):
        self.dialog.dismiss(force=True)
     def get_text_sign(self):
          email = self.ids.email_sign.text
          password = self.ids.passw_sign.text
          app = MDApp.get_running_app()
          answer = query(f'SELECT EMAIL FROM PROFILE WHERE EMAIL = {email}','select')
          salt = query(f'SELECT SALT FROM PROFILE WHERE EMAIL = {email}','select')
          password_db = query(f'SELECT PASSWORD FROM PROFILE WHERE EMAIL = {email}','select')
          hash = hashlib.sha512(bytes(password,encoding='utf-8')+bytes(salt,encoding='utf-8'))
          if answer == None:
               self.show_dialog('Данной учетной записи не существует')
          elif email == answer and hash == password_db:
               global current_user
               current_user = query(f'SELECT ID FROM PROFILE WHERE EMAIL = {email}','select')
               app.root.current = "main"
               app.root.transition.direction = "left"
class Registration(Tab):
     hint = StringProperty('Имя')
     def show_dialog(self,text):
          self.dialog = MDDialog(title='Ошибка',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='ОК',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self):
        self.dialog.dismiss(force=True)
     def check_text(self,instance, value):
          pass
          #instance.line_color_normal =  1,0,0,1
     def check_field(self):
          name = self.ids.name_reg.text
          lname = self.ids.lname_reg.text
          email = self.ids.email_reg.text
          city = self.ids.city_reg.text
          phone = self.ids.phone_reg.text
          password1 = self.ids.passw_reg1.text
          password2 = self.ids.passw_reg2.text
          match_name = re.fullmatch(r'^[А-Яа-яЁёa-zA-Z]+$', rf'{name}')
          match_lname = re.fullmatch(r'^[А-Яа-яЁёa-zA-Z]+$', rf'{lname}')
          match_city = re.fullmatch(r'^[А-Яа-яЁёa-zA-Z]+$', rf'{city}')
          match_city = re.fullmatch(r'^(8|\+7)[0-9]{10}$', rf'{phone}')
          match_password = re.fullmatch(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z@#$%-_]{6,20}$', rf'{password1}')
          if match_name != True:
               self.ids.name_reg.error = True
          if password1 == password2:
               self.correct_input()
          else:
               self.ids.pas_mes.disabled = False
     def correct_input(self):
          self.ids.pas_mes.disabled = True
          app = MDApp.get_running_app()
          name = self.ids.name_reg.text
          lname = self.ids.lname_reg.text
          email = self.ids.email_reg.text
          city = self.ids.city_reg.text
          phone = self.ids.phone_reg.text
          password = self.ids.passw_reg1.text
          salt_b = os.urandom(len(password)*2)
          dec_salt = salt_b.decode('utf-8',errors='ignore')
          #print(bytes(dec_salt,encoding='utf-8'))
          #print(password+bytes(dec_salt,encoding='utf-8'))
          hash = hashlib.sha512(bytes(password,encoding='utf-8')+bytes(dec_salt,encoding='utf-8'))
          hex_dig = hash.hexdigest()
          #print(hex_dig)
          query(f'INSERT INTO city VALUE({city})','insert')
          query(f'INSERT INTO profile (FIRST_NAME, LAST_NAME, EMAIL, CITY, PHONE_NUMBER, PASSWORD, SALT) VALUES ({name},{lname},{email},(SELECT ID FROM city where name = {city}),{phone},{hex_dig}),{dec_salt}','insert')
          global current_user
          current_user = query(f'SELECT ID FROM PROFILE WHERE EMAIL = {email}','select')
          app.root.current = "main"
          app.root.transition.direction = "left"
class About_me(Tab):
     pass
class Reviews(Tab):
     pass
class PopupMarker(Widget):
     pass
class Ad(RelativeLayout):
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
          self.stop()
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
               if 'nav_icon2' == current_id:
                    for i in range(5):
                         if f'nav_icon{i+1}' == current_id:
                              self.root.get_screen('service_list').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('service_list').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
               if 'nav_icon3' == current_id:
                    for i in range(5):
                         if f'nav_icon{i+1}' == current_id:
                              self.root.get_screen('add').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('add').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
               if 'nav_icon4' == current_id:
                    for i in range(5):
                         if f'nav_icon{i+1}' == current_id:
                              self.root.get_screen('notif_noreg').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('notif_noreg').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
               if 'nav_icon5' == current_id:
                    for i in range(5):
                         if f'nav_icon{i+1}' == current_id:
                              self.root.get_screen('profile').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('profile').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
     def transition_notif(self):
          log_in_user = False
          if log_in_user == False:
               #self.root.transition = NoTransition()
               self.root.current = 'notif_noreg'
     def transition_profile(self):
          log_in_user = True
          if log_in_user == False:
               #self.root.transition = NoTransition()
               self.root.current = 'profile_noreg'
          else:
               self.root.current = 'profile'
     def add_cards_ads(self):
          for i in range(10):
               card = Lost_card()
               card.bind(on_press=self.display_ad)
               self.root.ids.mainscreen.ids.lost_list.ids.container_lost.add_widget(card)
     def add_cards_services(self):
          for i in range(10):
               card = Service_card()
               card.bind(on_press=self.display_service)
               self.root.ids.service_list_screen.ids.container_service.add_widget(card)
     def display_ad(self, *args, **kwargs):
          self.root.current = 'ad'
     def display_service(self, *args, **kwargs):
          self.root.current = 'service'

     def on_start(self, **kwargs):
          self.check_internet()
          self.add_cards_ads()
          self.add_cards_services()
#kv = Builder.load_file("pets.kv")
if __name__ == '__main__':
     PetsApp().run()