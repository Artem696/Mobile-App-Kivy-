from attr import has
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
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
import mysql.connector
from mysql.connector import Error
import requests
import re
import hashlib
import os
from email_validate import validate


# Config.set('graphics', 'width', '414')
# Config.set('graphics', 'height', '736')
# Config.write()
current_user = None
def query(query,type,count='one'):
          try:
               with mysql.connector.connect(
                    host="127.0.0.1",
                    user=("root"),
                    password=("DcA4~6gfec7K"),
                    database="pets"
               ) as connection:
                    if type == "select":
                         if count == 'one':
                              with connection.cursor() as cursor:
                                   cursor.execute(query)
                                   result = cursor.fetchone()[0]
                                   return result
                         if count == 'all':
                              with connection.cursor() as cursor:
                                   cursor.execute(query)
                                   result = cursor.fetchall()
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
     def option_filter(self):
          self.type_ad = []
          self.kind_ad = []
          self.gender_ad = []
          if self.ids.type_cb_lost.state == 'down':
               self.type_ad.append('lost')
               print(self.ids.type_cb_lost.state)
          if self.ids.type_cb_detect.state == 'down':
               self.type_ad.append('detect')
               print(self.ids.type_cb_detect.state)
          self.city = self.ids.city.text
          if self.ids.kind_cb_cat.state == 'down':
               self.kind_ad.append('cat')
          if self.ids.kind_cb_dog.state == 'down':
               self.kind_ad.append('dog')
          if self.ids.gender_cb_man.state == 'down':
               self.kind_ad.append('man')
          if self.ids.gender_cb_wom.state == 'down':
               self.kind_ad.append('woman')
          if self.ids.gender_cb_unk.state == 'down':
               self.kind_ad.append('unknown')

class Ad_Screen(Screen):
     pass
class Service_List_Screen(Screen):
     pass
class Service_Screen(Screen):
     pass
class Profile_Screen(Screen):
     def download_data(self):
          global current_user
          if current_user != None:
               self.name = query(f'SELECT NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.ids.name_profile.text = self.name
               self.ids.lname_profile.text = self.lname
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
     def download_data(self):
          global current_user
          if current_user != None:
               self.name = query(f'SELECT NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.email = query(f'SELECT EMAIL FROM PROFILE WHERE ID = {current_user}','select')
               self.city = query(f'SELECT CITY FROM PROFILE WHERE ID = {current_user}','select')
               self.phone = query(f'SELECT PHONE_UMBER FROM PROFILE WHERE ID = {current_user}','select')
               self.ids.name_pd.text = self.name
               self.ids.lname_pd.text = self.lname
               self.ids.email_pd.text = self.email
               self.ids.city_pd.text = self.city
               self.ids.phone_pd.text = self.phone
class Change_Password_Screen(Screen):
     change = StringProperty('Изменить')
     def show_dialog(self,text):
          self.dialog = MDDialog(title='Ошибка',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='ОК',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
        self.dialog.dismiss(force=True)
     def check_pass(self,instance,value):
          self.app = MDApp.get_running_app()
          if self.app.root.current == 'change_password':
               for k, v in self.ids.items():
                    if v == instance:
                         if k == 'new_pass':
                              match_password = re.fullmatch(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z@#$%-_]{6,20}$', rf'{value}')
                              if match_password:
                                   self.ids.error_pass.disabled = True
                                   instance.line_color_normal =  0,0,0,0.12
                                   instance.line_color_focus = 0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0    
                                   self.ids.btn_save.disabled = False
                                   break
                              else:
                                   self.ids.error_pass.disabled = False
                                   instance.line_color_normal =  1,0,0,1
                                   instance.line_color_focus = 1,0,0,1
                                   self.ids.btn_save.disabled = True
                                   break
                         if k == 'repeat_new_pass':
                              if self.ids.new_pass.text == value:
                                   self.ids.btn_save.disabled = False
                                   self.ids.pas_mes.disabled = True
                              else:
                                   self.ids.btn_save.disabled = True
                                   self.ids.pas_mes.disabled = False

     def check_field(self):
          global current_user
          self.app = MDApp.get_running_app()
          self.old_password = self.ids.old_pass.text
          self.new_password = self.ids.new_pass.text
          self.repeat_new_password = self.ids.repeat_new_pass.text
          self.salt = query(f'SELECT SALT FROM PROFILE WHERE ID = {current_user}','select')
          self.password_db = query(f'SELECT PASSWORD FROM PROFILE WHERE ID = {current_user}','select')
          self.hash = hashlib.sha512(bytes(self.old_password,encoding='utf-8')+self.salt)
          self.hash_dig = self.hash.hexdigest()
          if not self.ids.old_pass.text or not self.ids.new_pass.text:
               self.show_dialog('Не все поля заполнены')
          else:
               if self.hash_dig != self.password_db:
                    self.show_dialog('Старый пароль не верный')
                    self.ids.old_pass.text = ''
                    self.ids.new_pass.text = ''
                    self.ids.repeat_new_pass.text = ''
               else:
                    if self.new_password != self.repeat_new_password:
                         self.ids.pas_mes.disabled = False
                         self.ids.new_pass.text = ''
                         self.ids.repeat_new_pass.text = ''
                    else:
                         salt_b = os.urandom(len(self.new_password)*2)
                         dec_salt = salt_b.decode('utf-8',errors='ignore')
                         hash = hashlib.sha512(bytes(self.new_password,encoding='utf-8')+bytes(dec_salt,encoding='utf-8'))
                         hex_dig = hash.hexdigest()
                         query(f'UPDATE PROFILE SET PASSWORD = {hex_dig}, SALT = {dec_salt}','update')
                         self.app.root.current = "data_personal"
                         self.app.root.transition.direction = "right"
                    
class WindowManager(ScreenManager):
     pass
class Lost_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Service_card(RoundedRectangularElevationBehavior,MDCard):
     text = StringProperty("1")
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
     def get_lon(self,zoom,x):
          pass
class Sign_in(Tab):
     def show_dialog(self,text):
          self.dialog = MDDialog(title='Ошибка',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='ОК',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
          self.dialog.dismiss(force=True)
     def get_text_sign(self):
          email = self.ids.email_sign.text
          password = self.ids.passw_sign.text
          app = MDApp.get_running_app()
          answer = query(f'SELECT EMAIL FROM PROFILE WHERE EMAIL = {email}','select')
          salt = query(f'SELECT SALT FROM PROFILE WHERE EMAIL = {email}','select')
          password_db = query(f'SELECT PASSWORD FROM PROFILE WHERE EMAIL = {email}','select')
          hash = hashlib.sha512(bytes(password,encoding='utf-8')+salt)
          hash_dig = hash.hexdigest()
          if answer == None:
               self.show_dialog('Данной учетной записи не существует')
          elif email == answer and hash_dig == password_db:
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
     def dialog_close(self,obj):
        self.dialog.dismiss(force=True)
     def check_text(self,instance, value, err=[]):
          self.app = MDApp.get_running_app()
          if self.app.root.current == 'login':
               for k, v in self.ids.items():
                    if v == instance:
                         if k == 'name_reg':
                              match_name = re.fullmatch(r'^[А-Яа-яЁёa-zA-Z]+$', rf'{value}')
                              if match_name:
                                   self.ids.error_name.disabled = True
                                   instance.line_color_normal =  0,0,0,0.12
                                   instance.line_color_focus = 0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0
                                   if k in err:
                                        err.remove(k)
                                   break
                              else:
                                   self.ids.error_name.disabled = False
                                   instance.line_color_normal =  1,0,0,1
                                   instance.line_color_focus = 1,0,0,1
                                   self.ids.btn_reg.disabled = True
                                   if k not in err:
                                        err.append(k)
                                   break
                         if k == 'lname_reg':
                              match_lname = re.fullmatch(r'^[А-Яа-яЁёa-zA-Z]+$', rf'{value}')
                              if match_lname:
                                   self.ids.error_lname.disabled = True
                                   instance.line_color_normal =  0,0,0,0.12
                                   instance.line_color_focus = 0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0
                                   if k in err:
                                        err.remove(k)
                                   break
                              else:
                                   self.ids.error_lname.disabled = False
                                   instance.line_color_normal =  1,0,0,1
                                   instance.line_color_focus = 1,0,0,1
                                   self.ids.btn_reg.disabled = True
                                   if k not in err:
                                        err.append(k)
                                   break
                         if k == 'email_reg':
                              if validate(email_address=f'{value}',check_format=True,check_blacklist=False,check_dns=False,dns_timeout=10,check_smtp=False,smtp_debug=False):
                                   self.ids.error_email.disabled = True
                                   instance.line_color_normal =  0,0,0,0.12
                                   instance.line_color_focus = 0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0
                                   if k in err:
                                        err.remove(k)
                                   break
                              else:
                                   self.ids.error_email.disabled = False
                                   instance.line_color_normal =  1,0,0,1
                                   instance.line_color_focus = 1,0,0,1
                                   self.ids.btn_reg.disabled = True
                                   if k not in err:
                                        err.append(k)
                                   break
                         if k == 'city_reg':
                              match_city = re.fullmatch(r'^[А-Яа-яЁёa-zA-Z]+$', rf'{value}')
                              if match_city:
                                   self.ids.error_city.disabled = True
                                   instance.line_color_normal =  0,0,0,0.12
                                   instance.line_color_focus = 0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0
                                   if k in err:
                                        err.remove(k)
                                   break
                              else:
                                   self.ids.error_city.disabled = False
                                   instance.line_color_normal =  1,0,0,1
                                   instance.line_color_focus = 1,0,0,1
                                   self.ids.btn_reg.disabled = True
                                   if k not in err:
                                        err.append(k)
                                   break
                         if k == 'phone_reg':
                              match_phone = re.fullmatch(r'^(8|\+7)[0-9]{10}$', rf'{value}')
                              if match_phone:
                                   self.ids.error_phone.disabled = True
                                   instance.line_color_normal =  0,0,0,0.12
                                   instance.line_color_focus = 0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0
                                   if k in err:
                                        err.remove(k)
                                   break
                              else:
                                   self.ids.error_phone.disabled = False
                                   instance.line_color_normal =  1,0,0,1
                                   instance.line_color_focus = 1,0,0,1
                                   self.ids.btn_reg.disabled = True
                                   if k not in err:
                                        err.append(k)
                                   break
                         if k == 'passw_reg1':
                              match_password = re.fullmatch(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z@#$%-_]{6,20}$', rf'{value}')
                              if match_password:
                                   self.ids.error_name.disabled = True
                                   instance.line_color_normal =  0,0,0,0.12
                                   instance.line_color_focus = 0.12941176470588237, 0.5882352941176471, 0.9529411764705882, 1.0
                                   if k in err:
                                        err.remove(k)
                                   break
                              else:
                                   self.ids.error_name.disabled = False
                                   instance.line_color_normal =  1,0,0,1
                                   instance.line_color_focus = 1,0,0,1
                                   self.ids.btn_reg.disabled = True
                                   if k not in err:
                                        err.append(k)
                                   break
               if not err:
                    self.ids.btn_reg.disabled = False
     def check_field(self,empty=[]):
          name = self.ids.name_reg.text
          lname = self.ids.lname_reg.text
          email = self.ids.email_reg.text
          city = self.ids.city_reg.text
          phone = self.ids.phone_reg.text
          password1 = self.ids.passw_reg1.text
          password2 = self.ids.passw_reg2.text
          for i in self.ids.keys():
               if i.find('reg') != -1:
                    if not self.ids[i].text:
                         if i not in empty:
                              empty.remove(i)
                         self.show_dialog('Не все поля заполнены')
                         break
                    else:
                         if i in empty:
                              empty.remove(i)
          if not empty: 
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
     name = StringProperty('Имя')
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
          self.count = query(f'SELECT COUNT(*) FROM AD','select')
          self.answer = query('SELECT * FROM AD ORDER BY ID DESC','select','all')
          for i in range(10):
               self.card = Lost_card()
               #self.image = 
               #self.date = query(f'SELECT CREATE_DATE FROM AD WHERE ID = {self.answer[i][0]}','select')
               #self.gender = query(f'SELECT GENDER FROM AD WHERE ID = {self.answer[i][0]}','select')
               #self.type = query(f'SELECT NAME FROM TYPE_AD WHERE ID = (SELECT TYPE FROM AD WHERE ID = {self.answer[i][0]}))','select')
               #self.card.ids.card_date.text = self.date
               #self.card.ids.gender.text = self.gender
               #self.card.ids.type.text = self.type
               self.card.bind(on_touch_down=self.display_ad)
               self.root.ids.mainscreen.ids.lost_list.ids.container_lost.add_widget(self.card)
     def add_cards_services(self):
          self.count = query(f'SELECT COUNT(*) FROM SERVICE','select')
          self.answer = query('SELECT * FROM SERVICE ORDER BY ID DESC','select','all')
          for i in range(10):
               self.card = Service_card()
               #self.create_date = query(f'SELECT CREATE_DATE FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
               # self.image = 
               # self.name = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.answer[i][0]}))','select')
               # self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.answer[i][0]}))','select')
               # self.city = query(f'SELECT CITY FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.answer[i][0]}))','select')
               # self.kind = query(f'SELECT NAME FROM KIND_SERVICE WHERE ID = (SELECT KIND FROM SERVICE WHERE ID = {self.answer[i][0]}))','select')
               # self.price = query(f'SELECT PRICE FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
               # self.card.ids.name_service_card.text = self.name + ' ' + self.lname
               # self.card.ids.city_service_card.text = self.city
               # self.card.ids.price_service_card.text = self.price
               #self.card.ids.kind_service_card.text = self.kind
               #self.card.ids.date_service_card.text = self.create_date
               self.card.bind(on_touch_down=self.display_service)
               self.root.ids.service_list_screen.ids.container_service.add_widget(self.card)
     def display_ad(self, card, touch):
          #self.root.ids.ad.ids.ad_container.ids.ad_image
          # self.create_date = card.ids.card_date.text
          # self.lat = query(f'SELECT LAT FROM AD WHERE CREATE_DATE = {self.create_date}','select')
          # self.lon = query(f'SELECT LON FROM AD WHERE CREATE_DATE = {self.create_date}','select')
          # self.kind = query(f'SELECT NAME FROM KIND_PET WHERE ID = (SELECT KIND_PETS FROM AD WHERE CREATE_DATE = {self.create_date})','select')
          # self.gender = query(f'SELECT GENDER FROM AD WHERE CREATE_DATE = {self.create_date}','select')
          # self.comment = query(f'SELECT TEXT FROM AD WHERE CREATE_DATE = {self.create_date}','select')
          # self.name = query(f'SELECT FIRST_NAME FROM AD WHERE CREATE_DATE = {self.create_date}','select')
          # self.phone_number = query(f'SELECT PHONE_NUMBER FROM AD WHERE CREATE_DATE = {self.create_date}','select')
          # self.root.ids.ad_screen.ids.ad_container.ids.ad_mapmarker.lat = 55.818
          # self.root.ids.ad_screen.ids.ad_container.ids.ad_mapmarker.lon = 37.3317
          # self.root.ids.ad.ids.ad_container.ids.ad_kind.text = self.type
          # self.root.ids.ad.ids.ad_container.ids.ad_gender.text = self.gender
          # self.root.ids.ad.ids.ad_container.ids.ad_text.text = self.comment
          # self.root.ids.ad.ids.ad_container.ids.ad_name.text = self.name
          # self.root.ids.ad.ids.ad_container.ids.ad_phone.text = self.phone_number
          self.root.current = 'ad'
     def display_service(self, card, touch):
          #self.root.ids.ad.ids.ad_container.ids.service_image
          self.create_date = card.ids.date_service_card.text
          self.name = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.create_date}))','select')
          self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.create_date}))','select')
          self.address = query(f'SELECT ADDRESS FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
          self.kind = query(f'SELECT NAME FROM KIND_SERVICE WHERE ID = (SELECT KIND FROM SERVICE WHERE ID = {self.create_date}))','select')
          self.price = query(f'SELECT PRICE FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
          
          self.root.ids.service_screen.ids.name_service.text = self.name + ' ' + self.lname
          self.root.ids.service_screen.ids.address_service.text = self.address
          self.root.ids.service_screen.ids.kind_service.text = self.kind
          self.root.ids.service_screen.ids.price_service.text = self.price
          
          self.kind_pet = query(f'SELECT NAME FROM KIND_PET WHERE ID = (SELECT KIND_PETS FROM SERVICE WHERE CREATE_DATE = {self.create_date})','select')
          self.age = query(f'SELECT AGE FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
          self.phone_number = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.create_date})','select')
          self.comment = query(f'SELECT ABOUT_ME FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
          if self.kind_pet == 'Собака' or self.kind_pet == 'Все':
               self.size_dog = query(f'SELECT SIZE_DOG FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
               self.root.ids.service_screen.ids.size_dog2_serv.text = self.size_dog
               self.root.ids.service_screen.ids.age_serv.text = self.age
               self.root.ids.service_screen.ids.phone_serv.text = self.phone_number
               self.root.ids.service_screen.ids.comment.text = self.comment
               self.medicine = query(f'SELECT MEDICINE FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
               self.injection = query(f'SELECT INJECTION FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
               self.control = query(f'SELECT CONTROL FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
               self.education = query(f'SELECT EDUCATION FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select') 
               if not self.medicine:
                    self.root.ids.service_screen.ids.medicine.disabled = True
               if not self.injection:
                    self.root.ids.service_screen.ids.injection.disabled = True
               if not self.control:
                    self.root.ids.service_screen.ids.control.disabled = True
               if not self.education:
                    self.root.ids.service_screen.ids.education.disabled = True
               else:
                    self.name_educ = query(f'SELECT NAME_EDUCATION FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select') 
                    self.root.ids.service_screen.ids.education.text = '- Профильное образование - '+ self.name_educ
               self.root.current = 'service'
          if self.kind_pet == 'Кошка':
               self.root.ids.service_screen.ids.size_dog1_serv.disabled = True
               self.root.ids.service_screen.ids.size_dog2_serv.disabled = True
               self.root.ids.service_screen.ids.age_serv.text = self.age
               self.root.ids.service_screen.ids.phone_serv.text = self.phone_number
               self.root.ids.service_screen.ids.comment.text = self.comment
               self.medicine = query(f'SELECT MEDICINE FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
               self.injection = query(f'SELECT INJECTION FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
               self.control = query(f'SELECT CONTROL FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select')
               self.education = query(f'SELECT EDUCATION FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select') 
               if not self.medicine:
                    self.root.ids.service_screen.ids.medicine.disabled = True
               if not self.injection:
                    self.root.ids.service_screen.ids.injection.disabled = True
               if not self.control:
                    self.root.ids.service_screen.ids.control.disabled = True
               if not self.education:
                    self.root.ids.service_screen.ids.education.disabled = True
               else:
                    self.name_educ = query(f'SELECT NAME_EDUCATION FROM SERVICE WHERE CREATE_DATE = {self.create_date}','select') 
                    self.root.ids.service_screen.ids.education.text = '- Профильное образование - '+ self.name_educ
               self.root.current = 'service'
               


     def on_start(self, **kwargs):
          self.check_internet()
          self.add_cards_ads()
          self.add_cards_services()
#kv = Builder.load_file("pets.kv")
if __name__ == '__main__':
     PetsApp().run()