from attr import has
import kivy
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView,MapMarkerPopup,MapMarker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.behaviors import TouchBehavior
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
import mysql.connector
from mysql.connector import Error
import requests
import re
import hashlib
import os
from email_validate import validate
from geopy.geocoders import Nominatim
from plyer import gps
from kivy.uix.popup import Popup
import io
import datetime
from kivy.core.image import Image as CoreImage 
import locale
import sqlite3
#from android.permissions import request_permissions, Permission



# Config.set('graphics', 'width', '414')
# Config.set('graphics', 'height', '736')
# Config.write()
locale.setlocale(locale.LC_TIME, 'ru')
current_user = None
def query(query,type,count='one',photo=None):
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
                         if photo is None:
                              with connection.cursor(buffered=True) as cursor:
                                   result = cursor.execute(query)
                                   connection.commit()
                         else:
                              with connection.cursor(buffered=True) as cursor:
                                   result = cursor.execute(query,(photo,))
                                   connection.commit()
          except Error as e:
               print(f"The error '{e}' occurred")
class StartScreen(Screen):
     global current_user
     def on_location(self, **kwargs):
          #self.lat = kwargs['lat']
          #self.lon = kwargs['lon']
          self.marker = MapMarker()
          self.marker.lat = 55.57255244187822#self.lat
          self.marker.lon = 42.03819546003002#self.lon
          self.marker.source = r'Image\me_marker.png'
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.lat = 55.57255244187822#self.lat
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.lon = 42.03819546003002#self.lon
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.add_marker(self.marker)
     def gps_locate(self):
          gps.configure(on_location=self.on_location)
          gps.start(1000, 0)
     def add_markers(self):
          # request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
          self.app = MDApp.get_running_app()
          self.count = query(f'SELECT COUNT(*) FROM AD','select')
          self.answer = query(f'SELECT * FROM AD ORDER BY ID DESC','select','all')
          self.on_location()
          if self.count != 0:
               for i in range(self.count):
               #for i in range(1):
                    self.marker = MapMarkerPopup()
                    self.marker_popup = PopupMarker()
                    self.marker_popup.size_hint = None,None
                    self.marker_popup.size = 250,250
                    self.marker_popup.ids.type_marker.text = query(f'SELECT NAME FROM TYPE_AD WHERE ID = (SELECT TYPE FROM AD WHERE ID = {self.answer[i][0]})','select')
                    self.bdata = query(f'SELECT PHOTO FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.data = io.BytesIO(self.bdata)
                    self.marker_popup.ids.img_marker.texture = CoreImage(self.data, ext = "png").texture
                    self.lat = query(f'SELECT LAT FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.lon = query(f'SELECT LON FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.marker.lat = self.lat
                    self.marker.lon = self.lon
                    self.marker.source = r'Image\marker.png'
                    self.marker.add_widget(self.marker_popup)
                    self.app.root.ids.mainscreen.ids.lost_map.ids.map.add_marker(self.marker)
class MainScreen(Screen):
     pass
class LoginScreen(Screen):
     pass
class Notification_NoReg(Screen):
     pass
class Notification_Screen(Screen):
     def open(self,card):
          self.app = MDApp.get_running_app()
          self.create_date = '2022-06-17 04:16:03'
          self.bdata = query(f'SELECT PHOTO FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.data = io.BytesIO(self.bdata)
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_image.texture = CoreImage(self.data, ext = "png").texture
          self.lat = query(f'SELECT LAT FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.lon = query(f'SELECT LON FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.kind = query(f'SELECT NAME FROM KIND_PET WHERE ID = (SELECT KIND_PETS FROM AD WHERE CREATE_DATE = "{self.create_date}")','select')
          self.gender = query(f'SELECT GENDER FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.comment = query(f'SELECT TEXT FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.fname = query(f'SELECT FIRST_NAME FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.phone_number = query(f'SELECT PHONE_NUMBER FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          if self.app.root.current == 'profile':
               self.app.root.ids.ad_screen.ids.ad_container.ids.btn_change.opacity = 1
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_date.text = self.create_date
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_map.lat = self.lat
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_map.lon = self.lon
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_mapmarker.lat = self.lat
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_mapmarker.lon = self.lon
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_kind.text = self.kind
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_gender.text = self.gender
          if self.comment == 'NULL':
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_text.text = '?????????????????????? ??????????????????????'
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_text.text = self.comment
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_name.text = self.fname
          self.app.root.ids.ad_screen.ids.ad_container.ids.ad_phone.text = self.phone_number
          self.app.root.current = 'ad'
     def notification(self):
          global current_user
          self.app = MDApp.get_running_app()
          #self.app.root.ids.notification_screen.container.clear_widgets()
          self.count_rev = query(f'select count(*) from REVIEW WHERE ID_PROFILE = {current_user}','select')
          self.count_com = query(f'select count(*) from COMMENT WHERE ID_PROFILE = 2','select')
          if int(self.ids.count_com.text) != self.count_com:
               self.notif = Notification_Card()
               self.notif.ids.textt.text = '???????????????? ?????????? ??????????????????????'
               self.app.root.ids.notification_screen.ids.container.add_widget(self.notif)
               self.date_ad = query(f'SELECT CREATE_DATE FROM AD WHERE ID = (SELECT ID_AD FROM COMMENT ORDER BY ID DESC LIMIT 1)','select','all')
               self.notif.ids.date.text = str(self.date_ad)
               self.notif.bind(on_press=self.open)
               self.ids.count_com.text = str(self.count_com)
          if int(self.ids.count_rev.text) != self.count_rev:
               self.notif = Notification_Card()
               self.notif.text = '???????????????? ?????????? ??????????'
               self.app.root.ids.notification_screen.container.add_widget(self.notif)
               self.ids.count_rev.text = self.count_rev
class Profile_NoReg(Screen):
     pass
class Service_Filter(Screen):
     global current_user
     def apply_filter(self):
          self.city = self.ids.city.text
          self.app = MDApp.get_running_app()
          if self.ids.kind_cb_overexposure.active:
               self.type_serv = '1'
          if self.ids.kind_cb_nanny.active:
               self.type_serv = '2'
          if self.ids.kind_cb_walk.active:
               self.type_serv = '3'
          if self.ids.kind_cb_overexposure.active and self.ids.kind_cb_nanny.active:
               self.type_serv = '1 OR 2'
          if self.ids.kind_cb_overexposure.active and self.ids.kind_cb_walk.active:
               self.type_serv = '1 OR 3'
          if self.ids.kind_cb_overexposure.active and self.ids.kind_cb_nanny.active and self.ids.kind_cb_walk.active:
               self.type_serv = '1 OR 2 OR 3'
          if self.ids.kind_cb_nanny.active and self.ids.kind_cb_walk.active:
               self.type_serv = '2 OR 3'
          if not self.ids.kind_cb_overexposure.active and not self.ids.kind_cb_nanny.active and not self.ids.kind_cb_walk.active:
               self.type_serv = '1 OR 2 OR 3'
          if self.ids.kind_pet_cat.active:
               self.kind = '1'
          if self.ids.kind_pet_dog.active:
               self.kind = '2'
          if self.ids.kind_pet_cat.active and self.ids.kind_pet_dog.active:
               self.kind = '3'
          if not self.ids.kind_pet_cat.active and not self.ids.kind_pet_dog.active:
               self.kind = '1 OR 2 OR 3'
          if self.ids.age_up_1.active:
               self.age = '"???? 1 ????????"'
          if self.ids.age_from_1.active:
               self.age = '"???????????? 1 ????????"'
          if self.ids.age_up_1.active and self.ids.age_from_1.active:
               self.age = '"??????????"'
          if not self.ids.age_up_1.active and not self.ids.age_from_1.active:
               self.age = '"???? 1 ????????" OR "???? 1 ????????" OR "??????????"'
          if self.ids.give_medicine.active:
               self.medicine = 1
          else:
               self.medicine = 0
          if self.ids.do_injection.active:
               self.injection = 1
          else:
               self.injection = 0
          if self.ids.control.active:
               self.control = 1
          else:
               self.control = 0
          if self.ids.education.active:
               self.education = 1
          else:
               self.education = 0
          if self.ids.kind_pet_dog.active:
               if self.ids.small_size.active:
                    self.size_dog = '"??????????????????"'
               if self.ids.medium_size.active:
                    self.size_dog = '"??????????????"'
               if self.ids.large_size.active:
                    self.size_dog = '"??????????????"'
               if self.ids.small_size.active and self.ids.medium_size.active:
                    self.size_dog = '"??????????????????" OR "??????????????"'
               if self.ids.small_size.active and self.ids.large_size.active:
                    self.size_dog = '"??????????????????" OR "??????????????"'
               if self.ids.small_size.active and self.ids.medium_size.active and self.ids.large_size.active:
                    self.size_dog = '"??????????????????" OR "??????????????" OR "??????????????"'
               if self.ids.medium_size.active and self.ids.large_size.active:
                    self.size_dog = '"??????????????" OR "??????????????"'
               if not self.ids.small_size.active and not self.ids.medium_size.active and not self.ids.large_size.active:
                    self.size_dog = '"??????????????????" OR "??????????????" OR "??????????????"'
               if self.city:
                    if self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE BETWEEN {self.ids.from_price.text} AND {self.ids.to_price.text}) AND (CITY = {self.city})','select','all')
                    if self.ids.from_price.text and not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE > {self.ids.from_price.text}) AND (CITY = {self.city})','select','all')
                    if not self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE < {self.ids.from_price.text}) AND (CITY = {self.city})','select','all')
                    if not self.ids.from_price.text and  not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (CITY = {self.city})','select','all')
               else:
                    if self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE BETWEEN {self.ids.from_price.text} AND {self.ids.to_price.text})','select','all')
                    if self.ids.from_price.text and not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE > {self.ids.from_price.text})','select','all')
                    if not self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE < {self.ids.from_price.text})','select','all')
                    if not self.ids.from_price.text and  not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education})','select','all')
               self.app.add_cards_services()
               self.app.root.current = 'service_list'
          if not self.ids.kind_pet_dog.active and self.ids.kind_pet_cat.active:
               if self.city:
                    if self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE BETWEEN {self.ids.from_price.text} AND {self.ids.to_price.text}) AND (CITY = {self.city})','select','all')
                    if self.ids.from_price.text and not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE > {self.ids.from_price.text}) AND (CITY = {self.city})','select','all')
                    if not self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE < {self.ids.from_price.text}) AND (CITY = {self.city})','select','all')
                    if not self.ids.from_price.text and  not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (SIZE_DOG = {self.size_dog}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (CITY = {self.city})','select','all')
               else:
                    if self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE BETWEEN {self.ids.from_price.text} AND {self.ids.to_price.text})','select','all')
                    if self.ids.from_price.text and not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE > {self.ids.from_price.text})','select','all')
                    if not self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE < {self.ids.from_price.text})','select','all')
                    if not self.ids.from_price.text and  not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education})','select','all')
               self.app.add_cards_services()
               self.app.root.current = 'service_list'
          if not self.ids.kind_pet_cat.active and not self.ids.kind_pet_dog.active:
               if self.city:
                    if self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE BETWEEN {self.ids.from_price.text} AND {self.ids.to_price.text}) AND (CITY = {self.city})','select','all')
                    if self.ids.from_price.text and not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE > {self.ids.from_price.text}) AND (CITY = {self.city})','select','all')
                    if not self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE < {self.ids.from_price.text}) AND (CITY = {self.city})','select','all')
                    if not self.ids.from_price.text and  not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (CITY = {self.city})','select','all')
               else:
                    if self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE BETWEEN {self.ids.from_price.text} AND {self.ids.to_price.text})','select','all')
                    if self.ids.from_price.text and not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE > {self.ids.from_price.text})','select','all')
                    if not self.ids.from_price.text and self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education}) AND (PRICE < {self.ids.from_price.text})','select','all')
                    if not self.ids.from_price.text and  not self.ids.to_price.text:
                         self.filter_id = query(f'SELECT ID FROM SERVICE WHERE (KIND = {self.type_serv}) AND (KIND_PETS = {self.kind}) AND (AGE = {self.age}) AND (MEDICINE = {self.medicine}) AND (INJECTION = {self.injection}) AND (CONTROL = {self.control}) AND (EDUCATION = {self.education})','select','all')
               self.app.add_cards_services()
               self.app.root.current = 'service_list'
     def visible_btn_reset(self,dt):
          if self.ids.btn_reset.opacity == 1:
               self.ids.btn_reset.opacity = 0
               self.ids.btn_reset.disabled = True
          else:
               self.ids.btn_reset.opacity = 1
               self.ids.btn_reset.disabled = False
     def reset_filter(self):
          self.app = MDApp.get_running_app()
          self.app.add_cards_services()
          self.app.root.current = 'service_list'
          Clock.schedule_once(self.visible_btn_reset, 0.5)
class Lost_Filter(Screen):
     def visible_btn_reset(self,dt):
          if self.ids.btn_reset.opacity == 1:
               self.ids.btn_reset.opacity = 0
               self.ids.btn_reset.disabled = True
          else:
               self.ids.btn_reset.opacity = 1
               self.ids.btn_reset.disabled = False
     def apply_filter(self):
          self.app = MDApp.get_running_app()
          #self.app.root.ids.ad_screen.ids.ad_container.ids.ad_date.text
          if self.ids.type_cb_lost.active:
               self.type = '1'
          if self.ids.type_cb_detect.active:
               self.type = '2'
          if self.ids.type_cb_detect.active and self.ids.type_cb_lost.active:
               self.type = '1 OR 2'
          if not self.ids.type_cb_detect.active and not self.ids.type_cb_lost.active:
               self.type = '1 OR 2'
          self.city = self.ids.city.text
          if self.ids.kind_cb_cat.active:
               self.kind = '1'
          if self.ids.kind_cb_dog.active:
               self.kind = '2'
          if self.ids.kind_cb_dog.active and self.ids.kind_cb_cat.active:
               self.kind = '1 OR 2'
          if not self.ids.kind_cb_dog.active and not self.ids.kind_cb_cat.active:
               self.kind = '1 OR 2'
          if self.ids.gender_cb_man.active:
               self.gender = '"??????????????" OR "????????????????????"'
          if self.ids.gender_cb_wom.active:
               self.gender = '"??????????????" OR "????????????????????"'
          if self.ids.gender_cb_wom.active and self.ids.gender_cb_man.active:
               self.gender = '"??????????????" OR "??????????????" OR "????????????????????"'
          if not self.ids.gender_cb_wom.active and not self.ids.gender_cb_man.active:
               self.gender = '"??????????????" OR "??????????????" OR "????????????????????"'
          if self.city:
               self.filter_id = query(f'SELECT ID FROM AD WHERE (TYPE = {self.type}) AND (KIND_PETS = {self.kind}) AND (GENDER = {self.gender}) AND (CITY = "{self.city}")','select','all')
          else:
               self.filter_id = query(f'SELECT ID FROM AD WHERE (TYPE = {self.type}) AND (KIND_PETS = {self.kind}) AND (GENDER = {self.gender})','select','all')
          self.app.add_cards_ads()
          self.app.root.current = 'main'
          Clock.schedule_once(self.visible_btn_reset, 0.5)

     def reset_filter(self):
          self.app = MDApp.get_running_app()
          self.app.add_cards_ads()
          self.app.root.current = 'main'
          Clock.schedule_once(self.visible_btn_reset, 0.5)
          
class Ad_Screen(Screen):
     def comment(self):
          global current_user
          self.app = MDApp.get_running_app()
          if current_user is None:
               self.app.ids.comment_screen.ids.btn.opacity = 0
               self.app.ids.comment_screen.ids.text_comment.opacity = 0
class Comment_Screen(Screen):
     global current_user
     def download_data(self):
          self.app = MDApp.get_running_app()
          self.answer = query('SELECT ID FROM COMMENT','select','all')
          self.count = query('select count(*) from COMMENT','select')
          if self.count > 6:
               self.height += (self.count-6)*100
               self.app.root.ids.comment_screen.ids.scroll.height = self.height
          self.com_container = GridLayout(cols=1,size_hint=(0.65, 0.94),pos_hint={'center_x': 0.5, 'y': 0.05},spacing='10dp')
          for i in range(self.count):
               self.comment = Comment_card()
               self.text = query(f'SELECT TEXT FROM COMMENT WHERE ID = {self.answer[i][0]}','select')
               self.name_user = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM COMMENT WHERE ID = {self.answer[i][0]})','select')
               self.date = query(f'SELECT CREATE_DATE FROM COMMENT WHERE ID = {self.answer[i][0]}','select')
               self.comment.ids.user.text = self.name_user
               self.comment.ids.text_card.text = self.text
               self.comment.ids.date_card.text = self.date.strftime('%d %B %Y, %H:%M')
               self.com_container.add_widget(self.comment)
          self.app.root.ids.comment_screen.ids.scroll.clear_widgets()
          self.app.root.ids.comment_screen.ids.scroll.add_widget(self.com_container)
     def send_comment(self):
          self.app = MDApp.get_running_app()
          self.comment = Comment_card()
          self.comment.ids.text_card.text = self.app.root.ids.comment_screen.ids.text_comment.text
          self.comment.ids.user.text = query(f"SELECT FIRST_NAME FROM PROFILE WHERE ID = {current_user}",'select')
          self.now = datetime.datetime.now()
          self.comment.ids.date_card.text = self.now.strftime('%d %B %Y, %H:%M')
          self.count_card = int(self.app.root.ids.comment_screen.ids.count_card.text)
          self.count_card += 1
          self.app.root.ids.comment_screen.ids.count_card.text = str(self.count_card)
          if self.count_card > 6:
               self.height = self.app.root.ids.comment_screen.ids.scroll.height
               self.height += 100
               self.app.root.ids.comment_screen.ids.scroll.height = self.height
          self.app.root.ids.comment_screen.ids.scroll.add_widget(self.comment)
          query(f'INSERT INTO COMMENT (ID_PROFILE,ID_AD,CREATE_DATE,TEXT) VALUES ({current_user},(SELECT ID FROM AD WHERE CREATE_DATE = "{self.app.root.ids.ad_screen.ids.ad_container.ids.ad_date.text}"),NOW(),"{self.comment.ids.text_card.text}")','insert')
class Review_Screen(Screen):
     def download_data(self):
          self.app = MDApp.get_running_app()
          self.answer = query('SELECT ID FROM REVIEW','select','all')
          self.count = query('select count(*) from REVIEW','select')
          if self.count > 6:
               self.height += (self.count-6)*100
               self.app.root.ids.review_screen.ids.scroll.height = self.height
          self.rev_container = GridLayout(cols=1,size_hint=(0.65, 0.94),pos_hint={'center_x': 0.5, 'y': 0.05},spacing='10dp')
          for i in range(self.count):
               self.review = Reviews_card()
               self.text = query(f'SELECT TEXT FROM COMMENT WHERE ID = {self.answer[i][0]}','select')
               self.name_user = query(f'SELECT CREATE_DATE FROM COMMENT WHERE ID = {self.answer[i][0]}','select')
               self.date = query(f'SELECT CREATE_DATE FROM COMMENT WHERE ID = {self.answer[i][0]}','select')
               self.review.ids.user.text = self.name_user
               self.review.ids.text_card.text = self.text
               self.review.ids.date_card.text = self.date.strftime('%d %B %Y, %H:%M')
               self.rev_container.add_widget(self.card)
          self.app.root.ids.review_screen.ids.scroll.clear_widgets()
          self.app.root.ids.review_screen.ids.scroll.add_widget(self.rev_container)
     def send_review(self):
          global current_user
          self.app = MDApp.get_running_app()
          self.review = Reviews_card()
          self.review.ids.text_card.text = self.app.root.ids.review_screen.ids.text_review.text
          self.now = datetime.datetime.now()
          self.review.ids.date_card.text = self.now.strftime('%d %B %Y, %H:%M')
          self.count_card = int(self.app.root.ids.review_screen.ids.count_card.text)
          self.count_card += 1
          self.app.root.ids.review_screen.ids.count_card.text = str(self.count_card)
          if self.count_card > 6:
               self.height = self.app.root.ids.review_screen.ids.scroll.height
               self.height += 100
               self.app.root.ids.review_screen.ids.scroll.height = self.height
          self.app.root.ids.review_screen.ids.review_container.add_widget(self.review)
          query(f'INSERT INTO REVIEW (ID_PROFILE,ID_SERVICE,CREATE_DATE,TEXT) VALUES ({current_user},(SELECT ID FROM AD WHERE CREATE_DATE = "{self.app.root.ids.service_screen.ids.date_service.text}"),CAST("{self.now.strftime("%d-%m-%Y %H:%M:%S")}" AS DateTime),{self.app.root.ids.review_screen.ids.text_review.text})','insert')
class Service_List_Screen(Screen):
     pass
class Service_Screen(Screen):
     def review(self):
          global current_user
          self.app = MDApp.get_running_app()
          if current_user is None:
               self.app.ids.review_screen.ids.btn.opacity = 0
               self.app.ids.review_screen.ids.text_comment.opacity = 0
class Profile_Screen(Screen):
     global current_user
     def removeall_ad(self):
          self.app = MDApp.get_running_app()
          rows = [i for i in self.app.root.ids.my_ad_screen.ids.container_lost.children]
          for row1 in rows:
               if isinstance(row1, MDCard):
                    self.app.root.ids.my_ad_screen.ids.container_lost.remove_widget(row1)
     def removeall_service(self):
          self.app = MDApp.get_running_app()
          rows = [i for i in self.app.root.ids.my_aervice_screen.ids.container_service.children]
          for row1 in rows:
               if isinstance(row1, MDCard):
                    self.app.root.ids.my_aervice_screen.ids.container_service.remove_widget(row1)
     def display_ad(self,card,touch):
          self.app = MDApp.get_running_app()
          if touch.opos[0]<580 or touch.opos[0]>590:
               self.create_date = card.ids.date.text
               self.bdata = query(f'SELECT PHOTO FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
               self.data = io.BytesIO(self.bdata)
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_image.texture = CoreImage(self.data, ext = "png").texture
               self.lat = query(f'SELECT LAT FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
               self.lon = query(f'SELECT LON FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
               self.kind = query(f'SELECT NAME FROM KIND_PET WHERE ID = (SELECT KIND_PETS FROM AD WHERE CREATE_DATE = "{self.create_date}")','select')
               self.gender = query(f'SELECT GENDER FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
               self.comment = query(f'SELECT TEXT FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
               self.fname = query(f'SELECT FIRST_NAME FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
               self.phone_number = query(f'SELECT PHONE_NUMBER FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
               if self.app.root.current == 'profile':
                    self.app.root.ids.ad_screen.ids.ad_container.ids.btn_change.opacity = 1
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_date.text = self.create_date
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_map.lat = self.lat
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_map.lon = self.lon
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_mapmarker.lat = self.lat
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_mapmarker.lon = self.lon
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_kind.text = self.kind
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_gender.text = self.gender
               if self.comment == 'NULL':
                    self.app.root.ids.ad_screen.ids.ad_container.ids.ad_text.text = '?????????????????????? ??????????????????????'
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_text.text = self.comment
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_name.text = self.fname
               self.app.root.ids.ad_screen.ids.ad_container.ids.ad_phone.text = self.phone_number
               self.app.root.current = 'ad'
     def display_service(self, card,touch):
          self.app = MDApp.get_running_app()
          if touch.opos[0]<580 or touch.opos[0]>590:
               self.create_date = card.ids.date.text
               self.bdata = query(f'SELECT PHOTO FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.data = io.BytesIO(self.bdata)
               self.app.root.ids.service_screen.ids.service_image.texture = CoreImage(self.data, ext = "png").texture
               self.fname = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
               self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
               self.address = query(f'SELECT ADDRESS FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.kind = query(f'SELECT NAME FROM KIND_SERVICE WHERE ID = (SELECT KIND FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
               self.price = query(f'SELECT PRICE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               
               self.app.root.ids.service_screen.ids.name_service.text = self.fname + ' ' + self.lname
               self.app.root.ids.service_screen.ids.address_service.text = self.address
               self.app.root.ids.service_screen.ids.kind_service.text = self.kind
               if self.kind == '??????????':
                    self.card.ids.type_price.text = '?????????????????? ???? 30 ??????????:'
               self.app.root.ids.service_screen.ids.price_service.text = self.price + ' ????????????'
               self.app.root.ids.service_screen.ids.date_service.text = self.create_date
               
               self.kind_pet = query(f'SELECT NAME FROM KIND_PET WHERE ID = (SELECT KIND_PETS FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
               self.age = query(f'SELECT AGE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.phone_number = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
               self.comment = query(f'SELECT ABOUT_ME FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               if self.kind_pet == '????????????' or self.kind_pet == '??????':
                    self.size_dog = query(f'SELECT SIZE_DOG FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
                    self.app.root.ids.service_screen.ids.size_dog2_serv.text = self.size_dog
                    self.app.root.ids.service_screen.ids.age_serv.text = self.age
                    self.app.root.ids.service_screen.ids.phone_serv.text = self.phone_number
                    self.app.root.ids.service_screen.ids.comment.text = self.comment
                    self.medicine = query(f'SELECT MEDICINE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
                    self.injection = query(f'SELECT INJECTION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
                    self.control = query(f'SELECT CONTROL FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
                    self.education = query(f'SELECT EDUCATION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select') 
                    if not self.medicine:
                         self.app.root.ids.service_screen.ids.medicine.disabled = True
                    if not self.injection:
                         self.app.root.ids.service_screen.ids.injection.disabled = True
                    if not self.control:
                         self.app.root.ids.service_screen.ids.control.disabled = True
                    if not self.education:
                         self.app.root.ids.service_screen.ids.education.disabled = True
                    else:
                         self.name_educ = query(f'SELECT NAME_EDUCATION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select') 
                         self.app.root.ids.service_screen.ids.education.text = '- ???????????????????? ?????????????????????? - '+ self.name_educ
                    self.app.root.current = 'service'
               if self.kind_pet == '??????????':
                    self.app.root.ids.service_screen.ids.size_dog1_serv.disabled = True
                    self.app.root.ids.service_screen.ids.size_dog2_serv.disabled = True
                    self.app.root.ids.service_screen.ids.age_serv.text = self.age
                    self.app.root.ids.service_screen.ids.phone_serv.text = self.phone_number
                    self.app.root.ids.service_screen.ids.comment.text = self.comment
                    self.medicine = query(f'SELECT MEDICINE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
                    self.injection = query(f'SELECT INJECTION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
                    self.control = query(f'SELECT CONTROL FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
                    self.education = query(f'SELECT EDUCATION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select') 
                    if not self.medicine:
                         self.app.root.ids.service_screen.ids.medicine.disabled = True
                    if not self.injection:
                         self.app.root.ids.service_screen.ids.injection.disabled = True
                    if not self.control:
                         self.app.root.ids.service_screen.ids.control.disabled = True
                    if not self.education:
                         self.app.root.ids.service_screen.ids.education.disabled = True
                    else:
                         self.name_educ = query(f'SELECT NAME_EDUCATION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select') 
                         self.app.root.ids.service_screen.ids.education.text = '- ???????????????????? ?????????????????????? - '+ self.name_educ
                    self.app.root.current = 'service'
     def download_my_ad(self):
          if current_user is not None:
               self.app = MDApp.get_running_app()
               self.count = query(f'SELECT COUNT(*) FROM AD WHERE ID_PROFILE = {current_user}','select')
               self.answer = query(f'SELECT * FROM AD WHERE ID_PROFILE = {current_user} ORDER BY ID DESC','select','all')
               self.removeall_ad()
               for i in range(self.count):
                    self.card = Lost_card()
                    if self.app.root.current == 'profile':
                         self.card.ids.btn_close.opacity = 1
                    self.bdata = query(f'SELECT PHOTO FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.data = io.BytesIO(self.bdata)
                    self.card.ids.card_image.texture = CoreImage(self.data, ext = "png").texture
                    self.date = query(f'SELECT CREATE_DATE FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.gender = query(f'SELECT GENDER FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.type = query(f'SELECT TYPE FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.city = query(f'SELECT CITY FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.card.ids.date.text = str(self.date)
                    self.card.ids.card_date.text = self.date.strftime('%d %B %Y, %H:%M')
                    self.card.ids.gender.text = self.gender
                    if self.type == 1 and self.gender == '??????????????':
                         self.card.ids.type.text = '????????????'
                    elif self.type == 1 and self.gender == '??????????????':
                         self.card.ids.type.text = '??????????????'
                    if self.type == 2 and self.gender == '??????????????':
                         self.card.ids.type.text = '??????????????'
                    elif self.type == 2 and self.gender == '??????????????':
                         self.card.ids.type.text = '????????????????'
                    self.card.ids.city.text = self.city
                    self.card.bind(on_touch_down=self.display_ad)
                    self.app.root.ids.my_ad_screen.ids.container_lost.add_widget(self.card)
     def download_my_service(self):
          if current_user is not None:
               self.app = MDApp.get_running_app()
               self.count = query(f'SELECT COUNT(*) FROM SERVICE WHERE ID_PROFILE = {current_user}','select')
               self.answer = query(f'SELECT * FROM SERVICE WHERE ID_PROFILE = {current_user} ORDER BY ID DESC','select','all')
               self.removeall_service()
               for i in range(self.count):
               #for i in range(1):
                    self.card = Service_card()
                    if self.app.root.current == 'profile':
                         self.card.ids.btn_close.opacity = 1
                    self.create_date = query(f'SELECT CREATE_DATE FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
                    self.bdata = query(f'SELECT PHOTO FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
                    self.data = io.BytesIO(self.bdata)
                    self.card.ids.card_image.texture = CoreImage(self.data, ext = "png").texture
                    self.fname = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.answer[i][0]})','select')
                    self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.answer[i][0]})','select')
                    self.city = query(f'SELECT CITY FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
                    self.kind = query(f'SELECT NAME FROM KIND_SERVICE WHERE ID = (SELECT KIND FROM SERVICE WHERE ID = {self.answer[i][0]})','select')
                    self.price = query(f'SELECT PRICE FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
                    self.card.ids.name_service_card.text = self.fname + ' ' + self.lname
                    self.card.ids.city_service_card.text = self.city
                    self.card.ids.kind_service_card.text = self.kind
                    if self.kind == '????????????????????':
                         self.card.ids.price_service_card.text = self.price+' ????????????/??????????'
                    if self.kind == '????????':
                         self.card.ids.price_service_card.text = self.price+' ????????????/??????????'
                    if self.kind == '??????????':
                         self.card.ids.price_service_card.text = self.price+' ????????????/30 ??????????'
                    self.card.ids.date.text = str(self.create_date)
                    self.card.ids.date_service_card.text = self.create_date.strftime('%d %B %Y, %H:%M')
                    self.card.bind(on_touch_down=self.display_service)
                    self.app.root.ids.my_aervice_screen.ids.container_service.add_widget(self.card)
     def download_data(self):
          if current_user != None:
               self.fname = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.bdata = query(f'SELECT AVATAR FROM PROFILE WHERE ID = {current_user}','select')
               self.data = io.BytesIO(self.bdata)
               self.ids.avatar.texture = CoreImage(self.data, ext = "png").texture
               self.ids.name_profile.text = self.fname
               self.ids.lname_profile.text = self.lname

class Add_Screen(Screen):
     global current_user
     def on_enter(self, **kwargs):
          if current_user is None:
               self.ids.add_lost_card.disabled = True
               self.ids.add_overexposure_card.disabled = True
               self.ids.add_nanny_card.disabled = True
               self.ids.add_walk_card.disabled = True
class Add_See_Screen(Screen):
     global current_user
     def on_enter(self, **kwargs):
          print("f")
          if current_user is None:
               print("f")
               # request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
               # request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
          else:
               # request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
               # request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
               self.ids.name.text = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.ids.phone.text = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = {current_user}','select')
     def on_location(self, **kwargs):
          self.lat = kwargs['lat']
          self.lon = kwargs['lon']
          self.geolocator = Nominatim(user_agent="Pets")
          self.location_r = self.geolocator.reverse(self.lat, self.lon)
          self.road = self.location_r.raw['address']['road']
          self.house = self.location_r.raw['address']['house_number']
          self.city = self.location_r.raw['address']['city']
          if self.house:
               self.ids.address.text = f'{self.road}, {self.house}, {self.city}'
          else:
               self.ids.address.text = f'{self.road}, {self.city}'
     def gps_locate(self):
          gps.configure(on_location=self.on_location)
          gps.start(1000, 0)
          
     def download_image(self):
          self.fc = FileChooser(title = '???????????????? ??????????????????????')
          self.fc.open()
     def show_dialog(self,text):
          self.dialog = MDDialog(title='????????????',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='????',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
          self.dialog.dismiss(force=True)
     def add_markers(self):
          # request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
          self.app = MDApp.get_running_app()
          self.count = query(f'SELECT COUNT(*) FROM AD','select')
          self.answer = query(f'SELECT * FROM AD ORDER BY ID DESC','select','all')
          #self.on_location()
          if self.count != 0:
               for i in range(self.count):
               #for i in range(1):
                    self.marker = MapMarkerPopup()
                    self.marker_popup = PopupMarker()
                    self.marker_popup.size_hint = None,None
                    self.marker_popup.size = 250,250
                    self.marker_popup.ids.type_marker.text = query(f'SELECT NAME FROM TYPE_AD WHERE ID = (SELECT TYPE FROM AD WHERE ID = {self.answer[i][0]})','select')
                    self.bdata = query(f'SELECT PHOTO FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.data = io.BytesIO(self.bdata)
                    self.marker_popup.ids.img_marker.texture = CoreImage(self.data, ext = "png").texture
                    self.lat = query(f'SELECT LAT FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.lon = query(f'SELECT LON FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.marker.lat = self.lat
                    self.marker.lon = self.lon
                    self.marker.source = r'Image\marker.png'
                    self.marker.add_widget(self.marker_popup)
                    self.app.root.ids.mainscreen.ids.lost_map.ids.map.add_marker(self.marker)
     def add_see(self):
          self.app = MDApp.get_running_app()
          self.add_markers()
          if not self.ids.kind_pet_cat.active and not self.ids.kind_pet_dog.active and not self.ids.gender_man.active and not self.ids.gender_wom.active and not self.ids.gender_unk.active:
               self.show_dialog('?????????????? ?????? ?? ?????? ??????????????????')
          else:
               if not self.ids.kind_pet_cat.active and not self.ids.kind_pet_dog.active:
                    self.show_dialog('?????????????? ?????? ??????????????????')
               else:
                    if not self.ids.gender_man.active and not self.ids.gender_wom.active and not self.ids.gender_unk.active:
                         self.show_dialog('?????????????? ?????? ??????????????????')
               if not self.ids.address.text and not self.ids.img.text:
                    self.show_dialog('?????????????? ?????????? ?? ????????')
               else:
                    if not self.ids.address.text:
                         self.show_dialog('?????????????? ??????????, ?????? ????????????')
                    else:
                         if not self.ids.img.text:
                              self.show_dialog('?????????????????? ???????? ??????????????????')

          if self.ids.kind_pet_cat.active:
               self.kind = 1
          if self.ids.kind_pet_dog.active:
               self.kind = 2
          if self.ids.gender_man.active:
               self.gender = '"??????????????"'
          if self.ids.gender_wom.active:
               self.gender = '"??????????????"'
          if self.ids.gender_unk.active:
               self.gender = '"????????????????????"'
          self.geolocator = Nominatim(user_agent="Pets")
          self.location = self.geolocator.geocode(self.ids.address.text)
          print(self.location.latitude, self.location.longitude)
          self.latitude = self.location.latitude
          self.longitude = self.location.longitude
          self.location_r = self.geolocator.reverse(f'{self.latitude}, {self.longitude}')
          self.city = self.location_r.raw['address']['city']
          if not self.ids.name:
               self.fname = 'NULL'
          else:
               self.fname = self.ids.name.text
          if not self.ids.phone:
               self.phone = 'NULL'
          else:
               self.phone = self.ids.phone.text
          if not self.ids.comment:
               self.comment = 'NULL'
          else:
               self.comment = self.ids.comment.text
          if current_user is None:
               self.id_user = 'NULL'
          else:
               self.id_user = current_user
          if self.ids.img.text:
               with open(self.ids.path_img.text, 'rb') as file:
                    self.blobData = file.read()
          query(f'INSERT INTO AD (TYPE,KIND_PETS,GENDER,PHOTO,LAT,LON,FIRST_NAME,PHONE_NUMBER,TEXT,ID_PROFILE,CREATE_DATE,CITY) VALUES (1,{self.kind},{self.gender},%s,{self.location.latitude},{self.location.longitude},"{self.fname}","{self.phone}","{self.comment}",{self.id_user},NOW(),"{self.city}")','insert',photo=self.blobData)
          #gps.stop()
          self.app.add_cards_ads()
          self.add_markers()
          self.app.root.current = 'main'
class Add_Lost_Screen(Screen):
     global current_user
     def on_enter(self, **kwargs):
          print("f")
          if current_user is None:
               print("f")
               # request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
          else:
               # request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
               self.ids.name.text = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.ids.phone.text = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = {current_user}','select')
     def download_image(self):
          self.fc = FileChooser(title = '???????????????? ??????????????????????')
          self.fc.open()
     def show_dialog(self,text):
          self.dialog = MDDialog(title='????????????',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='????',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
        self.dialog.dismiss(force=True)
     def add_markers(self):
          # request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
          self.app = MDApp.get_running_app()
          self.count = query(f'SELECT COUNT(*) FROM AD','select')
          self.answer = query(f'SELECT * FROM AD ORDER BY ID DESC','select','all')
          #self.on_location()
          if self.count != 0:
               for i in range(self.count):
               #for i in range(1):
                    self.marker = MapMarkerPopup()
                    self.marker_popup = PopupMarker()
                    self.marker_popup.size_hint = None,None
                    self.marker_popup.size = 250,250
                    self.marker_popup.ids.type_marker.text = query(f'SELECT NAME FROM TYPE_AD WHERE ID = (SELECT TYPE FROM AD WHERE ID = {self.answer[i][0]})','select')
                    self.bdata = query(f'SELECT PHOTO FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.data = io.BytesIO(self.bdata)
                    self.marker_popup.ids.img_marker.texture = CoreImage(self.data, ext = "png").texture
                    self.lat = query(f'SELECT LAT FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.lon = query(f'SELECT LON FROM AD WHERE ID = {self.answer[i][0]}','select')
                    self.marker.lat = self.lat
                    self.marker.lon = self.lon
                    self.marker.source = r'Image\marker.png'
                    self.marker.add_widget(self.marker_popup)
                    self.app.root.ids.mainscreen.ids.lost_map.ids.map.add_marker(self.marker)
     def apply_filter(self):
          self.app = MDApp.get_running_app()
          if not self.ids.kind_pet_cat.active and not self.ids.kind_pet_dog.active and not self.ids.gender_man.active and not self.ids.gender_wom.active and not self.ids.gender_unk.active:
               self.show_dialog('?????????????? ?????? ?? ?????? ??????????????????')
          else:
               if not self.ids.kind_pet_cat.active and not self.ids.kind_pet_dog.active:
                    self.show_dialog('?????????????? ?????? ??????????????????')
               else:
                    if not self.ids.gender_man.active and not self.ids.gender_wom.active and not self.ids.gender_unk.active:
                         self.show_dialog('?????????????? ?????? ??????????????????')
          if not self.ids.address.text and not self.ids.img.text:
               self.show_dialog('?????????????? ?????????? ?? ????????')
          else:
               if not self.ids.address.text:
                    self.show_dialog('?????????????? ??????????, ?????? ????????????')
               else:
                    if not self.ids.img.text:
                         self.show_dialog('?????????????????? ???????? ??????????????????')
          if self.ids.kind_pet_cat.active:
               self.kind = '1'
          if self.ids.kind_pet_dog.active:
               self.kind = '2'
          if self.ids.gender_man.active:
               self.gender = '"??????????????"'
          if self.ids.gender_wom.active:
               self.gender = '"??????????????"'
          self.geolocator = Nominatim(user_agent="Pets")
          self.location = self.geolocator.geocode(self.ids.address.text)
          self.latitude = self.location.latitude
          self.longitude = self.location.longitude
          self.location_r = self.geolocator.reverse(f'{self.latitude}, {self.longitude}')
          self.city = self.location_r.raw['address']['city']
          if not self.ids.name.text:
               self.fname = 'NULL'
          else:
               self.fname = self.ids.name.text
          if not self.ids.phone.text:
               self.phone = 'NULL'
          else:
               self.phone = self.ids.phone.text
          if self.ids.comment.text:
               self.comment = 'NULL'
          else:
               self.comment = self.ids.comment.text
          if current_user is None:
               self.id_user = 'NULL'
          else:
               self.id_user = current_user
          self.nickname = self.ids.nackname.text
          if self.ids.img.text:
               with open(self.ids.path_img.text, 'rb') as file:
                    self.blobData = file.read()
          query(f'INSERT INTO AD (TYPE,KIND_PETS,GENDER,PHOTO,LAT,LON,FIRST_NAME,PHONE_NUMBER,TEXT,ID_PROFILE,CREATE_DATE,NICKNAME,CITY) VALUES (2,{self.kind},{self.gender},%s,{self.location.latitude},{self.location.longitude},"{self.fname}","{self.phone}","{self.comment}",{self.id_user},NOW(),"{self.nickname}","{self.city}")','insert',photo=self.blobData)
          self.app.add_cards_ads()
          self.add_markers()
          self.app.root.current = 'main'
class Add_Overexposure_Screen(Screen):
     global current_user
     def on_enter(self, **kwargs):
          self.ids.fname.text = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = {current_user}','select')
          self.ids.lname.text = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = {current_user}','select')
          self.ids.phone.text = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = {current_user}','select')
     def on_location(self, **kwargs):
          self.lat = kwargs['lat']
          self.lon = kwargs['lon']
          self.geolocator = Nominatim(user_agent="Pets")
          self.location_r = self.geolocator.reverse(self.lat, self.lon)
          self.road = self.location_r.raw['address']['road']
          self.house = self.location_r.raw['address']['house_number']
          self.city = self.location_r.raw['address']['city']
          if self.house:
               self.ids.address.text = f'{self.road}, {self.house}, {self.city}'
          else:
               self.ids.address.text = f'{self.road}, {self.city}'
     def gps_locate(self):
          gps.configure(on_location=self.on_location)
          gps.start(1000, 0)
     def download_image(self):
          self.fc = FileChooser(title = '???????????????? ??????????????????????')
          self.fc.open()
     def show_dialog(self,text):
          self.dialog = MDDialog(title='????????????',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='????',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
        self.dialog.dismiss(force=True)
     def add(self):
          self.app = MDApp.get_running_app()
          if not self.ids.address.text and not self.ids.img.text:
               self.show_dialog('?????????????? ?????????? ?? ????????')
          else:
               if not self.ids.address.text:
                    self.show_dialog('?????????????? ??????????, ?????? ????????????')
               else:
                    if not self.ids.img.text:
                         self.show_dialog('?????????????????? ???????? ??????????????????')
                    else:
                         self.fname = self.ids.fname.text
                         self.lname = self.ids.lname.text
                         self.phone_number = self.ids.phone.text
                         self.geolocator = Nominatim(user_agent="Pets")
                         self.location = self.geolocator.geocode(self.ids.address.text)
                         self.latitude = self.location.latitude
                         self.longitude = self.location.longitude
                         self.location_r = self.geolocator.reverse(f'{self.latitude}, {self.longitude}')
                         self.city = self.location_r.raw['address']['city']
                         self.address = self.ids.address.text
                         if self.ids.kind_cb_cat.active:
                              self.kind = '1'
                         if self.ids.kind_cb_dog.active:
                              self.kind = '2'
                         if self.ids.kind_cb_all.active:
                              self.kind = '3'
                         if self.ids.kind_cb_dog.active or self.ids.kind_cb_all.active:
                              if self.ids.size_small.active:
                                   self.size_dog = '??????????????????'
                              if self.ids.size_medium.active:
                                   self.size_dog = '??????????????'
                              if self.ids.size_large.active:
                                   self.size_dog = '??????????????'
                              if self.ids.size_small.active and self.ids.size_medium.active:
                                   self.size_dog = '?????????????????? ?? ??????????????'
                              if self.ids.size_small.active and self.ids.size_medium.active:
                                   self.size_dog = '?????????????????? ?? ??????????????'
                              if self.ids.size_medium.active and self.ids.size_large.active:
                                   self.size_dog = '?????????????? ?? ??????????????'
                              if self.ids.size_all.active:
                                   self.size_dog = '??????????'
                         else:
                              self.size_dog = 'NULL'
                         if self.ids.age_from_1.active:
                              self.age = '???? 1 ????????'
                         if self.ids.age_up_1.active:
                              self.age = '???????????? 1 ????????'
                         if self.ids.age_all.active:
                              self.age = '??????????'
                         if self.ids.medicine.active:
                              self.medicine = 1
                         else:
                              self.medicine = 0
                         if self.ids.injection.active:
                              self.injection = 1
                         else:
                              self.injection = 0
                         if self.ids.control.active:
                              self.control = 1
                         else:
                              self.control = 0
                         if self.ids.education.active:
                              self.education = 1
                              self.name_educ = self.ids.name_educ.text
                         else:
                              self.education = 0
                              self.name_educ = 'NULL'
                         if self.ids.comment.text:
                              self.comment = self.ids.comment.text
                         else:
                              self.comment = 'NULL'
                         self.price = self.ids.price.text
                         if self.ids.img.text:
                              with open(self.ids.path_img.text, 'rb') as file:
                                   self.blobData = file.read()
                         else:
                              with open(r'Image\overexposure_add.png', 'rb') as file:
                                   self.blobData = file.read()
                         query(f'INSERT INTO SERVICE (KIND,KIND_PETS,SIZE_DOG,AGE,ID_PROFILE,MEDICINE,INJECTION,CONTROL,EDUCATION,NAME_EDUCATION,ADDRESS,CITY,PRICE,ABOUT_ME,CREATE_DATE,PHOTO) VALUES (1,"{self.kind}","{self.size_dog}","{self.age}","{current_user}",{self.medicine},{self.injection},{self.control},{self.education},"{self.name_educ}","{self.address}","{self.city}","{self.price}","{self.comment}",NOW(),%s)','insert',photo=self.blobData)
                         #gps.stop()
                         self.app.add_cards_services()
     def active_cat(self):
          if self.ids.kind_cb_cat.active and self.ids.kind_cb_all.active:
               self.ids.kind_cb_all.active = False
     def active_dog(self):
          if self.ids.kind_cb_dog.active and self.ids.kind_cb_all.active:
               self.ids.kind_cb_all.active = False
     def active_all(self):
          if self.ids.kind_cb_cat.active and self.ids.kind_cb_dog.active:
               self.ids.kind_cb_all.active = True
               self.ids.kind_cb_cat.active = False
               self.ids.kind_cb_dog.active = False
     def active_size_all(self):
          if self.ids.size_small.active and self.ids.size_medium.active and self.ids.size_large.active:
               self.ids.size_all.active = True
               self.ids.size_small.active = False
               self.ids.size_medium.active = False
               self.ids.size_large.active = False
     def active_size_large(self):
          if self.ids.size_large.active and self.ids.size_all.active:
               self.ids.size_all.active = False
     def active_size_medium(self):
          if self.ids.size_medium.active and self.ids.size_all.active:
               self.ids.size_all.active = False
     def active_size_small(self):
          if self.ids.size_small.active and self.ids.size_all.active:
               self.ids.size_all.active = False
     def active_age_all(self):
          if self.ids.age_from_1.active and self.ids.age_up_1.active:
               self.ids.age_all.active = True
               self.ids.age_from_1.active = False
               self.ids.age_up_1.active = False
     def active_age_from_1(self):
          if self.ids.age_from_1.active and self.ids.age_all.active:
               self.ids.age_all.active = False
     def active_age_up_1(self):
          if self.ids.age_up_1.active and self.ids.age_all.active:
               self.ids.age_all.active = False
     def press_education(self):
          if self.ids.education.active:
               self.ids.name_educ.opacity = 1
          else:
               self.ids.name_educ.opacity = 0

class Add_Nanny_Screen(Screen):
     def on_enter(self, **kwargs):
          self.ids.fname.text = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = {current_user}','select')
          self.ids.lname.text = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = {current_user}','select')
          self.ids.phone.text = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = {current_user}','select')
     def on_location(self, **kwargs):
          self.lat = kwargs['lat']
          self.lon = kwargs['lon']
          self.geolocator = Nominatim(user_agent="Pets")
          self.location_r = self.geolocator.reverse(self.lat, self.lon)
          self.road = self.location_r.raw['address']['road']
          self.house = self.location_r.raw['address']['house_number']
          self.city = self.location_r.raw['address']['city']
          if self.house:
               self.ids.address.text = f'{self.road}, {self.house}, {self.city}'
          else:
               self.ids.address.text = f'{self.road}, {self.city}'
     def gps_locate(self):
          gps.configure(on_location=self.on_location)
          gps.start(1000, 0)
     def download_image(self):
          self.fc = FileChooser(title = '???????????????? ??????????????????????')
          self.fc.open()
     def show_dialog(self,text):
          self.dialog = MDDialog(title='????????????',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='????',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
        self.dialog.dismiss(force=True)
     def add(self):
          if not self.ids.address.text and not self.ids.img.text:
               self.show_dialog('?????????????? ?????????? ?? ????????')
          else:
               if not self.ids.address.text:
                    self.show_dialog('?????????????? ??????????, ?????? ????????????')
               else:
                    if not self.ids.img.text:
                         self.show_dialog('?????????????????? ???????? ??????????????????')
                    else:
                         self.geolocator = Nominatim(user_agent="Pets")
                         self.location = self.geolocator.geocode(self.ids.address.text)
                         self.location_r = self.geolocator.reverse(self.location.latitude, self.location.longitude)
                         self.city = self.location_r.raw['address']['city']
                         self.address = self.ids.address.text
                         if self.ids.kind_cb_cat.active:
                              self.kind = '1'
                         if self.ids.kind_cb_dog.active:
                              self.kind = '2'
                         if self.ids.kind_cb_all.active:
                              self.kind = '3'
                         if self.ids.kind_cb_dog.active or self.ids.kind_cb_all.active:
                              if self.ids.size_small.active:
                                   self.size_dog = '??????????????????'
                              if self.ids.size_medium.active:
                                   self.size_dog = '??????????????'
                              if self.ids.size_large.active:
                                   self.size_dog = '??????????????'
                              if self.ids.size_small.active and self.ids.size_medium.active:
                                   self.size_dog = '?????????????????? ?? ??????????????'
                              if self.ids.size_small.active and self.ids.size_medium.active:
                                   self.size_dog = '?????????????????? ?? ??????????????'
                              if self.ids.size_medium.active and self.ids.size_large.active:
                                   self.size_dog = '?????????????? ?? ??????????????'
                              if self.ids.size_all.active:
                                   self.size_dog = '??????????'
                         else:
                              self.size_dog = 'NULL'
                         if self.ids.age_from_1.active:
                              self.age = '???? 1 ????????'
                         if self.ids.age_up_1.active:
                              self.age = '???????????? 1 ????????'
                         if self.ids.age_all.active:
                              self.age = '??????????'
                         if self.ids.medicine.active:
                              self.medicine = 1
                         else:
                              self.medicine = 0
                         if self.ids.injection.active:
                              self.injection = 1
                         else:
                              self.injection = 0
                         if self.ids.control.active:
                              self.control = 1
                         else:
                              self.control = 0
                         if self.ids.education.active:
                              self.education = 1
                              self.name_educ = self.ids.name_educ.text
                         else:
                              self.education = 0
                              self.name_educ = 'NULL'
                         if self.ids.comment.text:
                              self.comment = self.ids.comment.text
                         else:
                              self.comment = 'NULL'
                         self.price = self.ids.price.text
                         if self.ids.img.text:
                              with open(self.ids.path_img.text, 'rb') as file:
                                   self.blobData = file.read()
                         else:
                              with open(r'Image\nanny_add.png', 'rb') as file:
                                   self.blobData = file.read()
                         query(f'INSERT INTO SERVICE (KIND,KIND_PETS,SIZE_DOG,AGE,ID_PROFILE,MEDICINE,INJECTION,CONTROL,EDUCATION,NAME_EDUCATION,ADDRESS,CITY,PRICE,ABOUT_ME,CREATE_DATE,PHOTO) VALUES (1,{self.kind},{self.size_dog},{self.age},{current_user},{self.medicine},{self.injection},{self.control},{self.education},{self.name_educ},{self.address},{self.city},{self.price},{self.comment},NOW(),%s)','insert',photo=self.blobData)
                         gps.stop()
     def active_cat(self):
          if self.ids.kind_cb_cat.active and self.ids.kind_cb_all.active:
               self.ids.kind_cb_all.active = False
     def active_dog(self):
          if self.ids.kind_cb_dog.active and self.ids.kind_cb_all.active:
               self.ids.kind_cb_all.active = False
     def active_all(self):
          if self.ids.kind_cb_cat.active and self.ids.kind_cb_dog.active:
               self.ids.kind_cb_all.active = True
               self.ids.kind_cb_cat.active = False
               self.ids.kind_cb_dog.active = False
     def active_size_all(self):
          if self.ids.size_small.active and self.ids.size_medium.active and self.ids.size_large.active:
               self.ids.size_all.active = True
               self.ids.size_small.active = False
               self.ids.size_medium.active = False
               self.ids.size_large.active = False
     def active_size_large(self):
          if self.ids.size_large.active and self.ids.size_all.active:
               self.ids.size_all.active = False
     def active_size_medium(self):
          if self.ids.size_medium.active and self.ids.size_all.active:
               self.ids.size_all.active = False
     def active_size_small(self):
          if self.ids.size_small.active and self.ids.size_all.active:
               self.ids.size_all.active = False
     def active_age_all(self):
          if self.ids.age_from_1.active and self.ids.age_up_1.active:
               self.ids.age_all.active = True
               self.ids.age_from_1.active = False
               self.ids.age_up_1.active = False
     def active_age_from_1(self):
          if self.ids.age_from_1.active and self.ids.age_all.active:
               self.ids.age_all.active = False
     def active_age_up_1(self):
          if self.ids.age_up_1.active and self.ids.age_all.active:
               self.ids.age_all.active = False
     def press_education(self):
          if self.ids.education.active:
               self.ids.name_educ.opacity = 1
          else:
               self.ids.name_educ.opacity = 0
class Add_Walk_Screen(Screen):
     def on_enter(self, **kwargs):
          self.ids.fname.text = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = {current_user}','select')
          self.ids.lname.text = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = {current_user}','select')
          self.ids.phone.text = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = {current_user}','select')
     def download_image(self):
          self.fc = FileChooser(title = '???????????????? ??????????????????????')
          self.fc.open()
     def show_dialog(self,text):
          self.dialog = MDDialog(title='????????????',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='????',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
        self.dialog.dismiss(force=True)
     def add(self):
          self.geolocator = Nominatim(user_agent="Pets")
          self.location = self.geolocator.geocode(self.ids.address.text)
          self.location_r = self.geolocator.reverse(self.location.latitude, self.location.longitude)
          self.city = self.location_r.raw['address']['city']
          self.address = self.ids.address.text
          if self.ids.size_small.active:
               self.size_dog = '??????????????????'
          if self.ids.size_medium.active:
               self.size_dog = '??????????????'
          if self.ids.size_large.active:
               self.size_dog = '??????????????'
          if self.ids.size_small.active and self.ids.size_medium.active:
               self.size_dog = '?????????????????? ?? ??????????????'
          if self.ids.size_small.active and self.ids.size_medium.active:
               self.size_dog = '?????????????????? ?? ??????????????'
          if self.ids.size_medium.active and self.ids.size_large.active:
               self.size_dog = '?????????????? ?? ??????????????'
          if self.ids.size_all.active:
               self.size_dog = '??????????'
          if self.ids.comment.text:
               self.comment = self.ids.comment.text
          else:
               self.comment = 'NULL'
          self.price = self.ids.price.text
          if self.ids.img.text:
               with open(self.ids.path_img.text, 'rb') as file:
                    self.blobData = file.read()
          else:
               with open(r'Image\walk_add.png', 'rb') as file:
                    self.blobData = file.read()
          query(f'INSERT INTO SERVICE (KIND,SIZE_DOG,ID_PROFILE,`ADDRESS`,`CITY`,`PRICE`,`ABOUT_ME`,`CREATE_DATE`,PHOTO) VALUES (1,{self.size_dog},{current_user},{self.address},{self.city},{self.price},{self.comment},NOW(),%s)','insert',photo=self.blobData)
     def active_size_all(self):
          if self.ids.size_small.active and self.ids.size_medium.active and self.ids.size_large.active:
               self.ids.size_all.active = True
               self.ids.size_small.active = False
               self.ids.size_medium.active = False
               self.ids.size_large.active = False
     def active_size_large(self):
          if self.ids.size_large.active and self.ids.size_all.active:
               self.ids.size_all.active = False
     def active_size_medium(self):
          if self.ids.size_medium.active and self.ids.size_all.active:
               self.ids.size_all.active = False
     def active_size_small(self):
          if self.ids.size_small.active and self.ids.size_all.active:
               self.ids.size_all.active = False
class My_Ad_Screen(Screen):
     pass
class My_Service_Screen(Screen):
     pass
class Personal_Data(Screen):
     change = StringProperty('???????????????? ????????????')
     global current_user
     def download_image(self):
          self.fc = FileChooser(title = '???????????????? ??????????????????????')
          self.fc.open()
     def save_change(self):
          with open(self.ids.profile_icon.icon, 'rb') as file:
               self.blobData = file.read()
          query(f'UPDATE PROFILE SET FIRST_NAME="{self.ids.name_pd.text}",LAST_NAME="{self.ids.lname_pd.text}",AVATAR=%s,EMAIL="{self.ids.email_pd.text}",PHONE_NUMBER="{self.ids.phone_pd.text}" WHERE ID = {current_user}','update',photo=self.blobData)
     def download_data(self):
          if current_user != None:
               self.fname = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = {current_user}','select')
               self.email = query(f'SELECT EMAIL FROM PROFILE WHERE ID = {current_user}','select')
               #self.city = query(f'SELECT CITY FROM PROFILE WHERE ID = {current_user}','select')
               self.phone = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = {current_user}','select')
               self.ids.name_pd.text = self.fname
               self.ids.lname_pd.text = self.lname
               self.ids.email_pd.text = self.email
               #self.ids.city_pd.text = self.city
               self.ids.phone_pd.text = self.phone
class Change_Password_Screen(Screen):
     change = StringProperty('????????????????')
     def show_dialog(self,text):
          self.dialog = MDDialog(title='????????????',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='????',on_release = self.dialog_close)]
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
          self.hash = hashlib.sha512(bytes(self.old_password,encoding='utf-8')+bytes(self.salt,encoding='utf-8'))
          self.hash_dig = self.hash.hexdigest()
          if not self.ids.old_pass.text or not self.ids.new_pass.text:
               self.show_dialog('???? ?????? ???????? ??????????????????')
          else:
               if self.hash_dig != self.password_db:
                    self.show_dialog('???????????? ???????????? ???? ????????????')
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
                         query(f'UPDATE PROFILE SET PASSWORD = "{hex_dig}", SALT = "{dec_salt}" WHERE ID = {current_user}','update')
                         self.app.root.current = "data_personal"
                         self.app.root.transition.direction = "right"
                    
class WindowManager(ScreenManager):
     pass

class FileChooser(Popup):
     def selected(self,filename):
          self.path_img = filename[0]
          self.name_img = os.path.basename(filename[0])
          self.app = MDApp.get_running_app()
          if self.app.root.current == 'add_see':
               self.app.root.ids.add_see_screen.ids.img.text = self.name_img
               self.app.root.ids.add_see_screen.ids.path_img.text = self.path_img
               self.app.root.ids.add_see_screen.ids.img.opacity = 1
          if self.app.root.current == 'add_lost':
               self.app.root.ids.add_lost_screen.ids.img.text = self.name_img
               self.app.root.ids.add_lost_screen.ids.path_img.text = self.path_img
               self.app.root.ids.add_lost_screen.ids.img.opacity = 1
          if self.app.root.current == 'add_overexposure':
               self.app.root.ids.add_overexposure_screen.ids.img.text = self.name_img
               self.app.root.ids.add_overexposure_screen.ids.path_img.text = self.path_img
               self.app.root.ids.add_overexposure_screen.ids.img.opacity = 1
          if self.app.root.current == 'add_nanny':
               self.app.root.ids.add_nanny_screen.ids.img.text = self.name_img
               self.app.root.ids.add_nanny_screen.ids.path_img.text = self.path_img
               self.app.root.ids.add_nanny_screen.ids.img.opacity = 1
          if self.app.root.current == 'add_walk':
               self.app.root.ids.add_walk_screen.ids.img.text = self.name_img
               self.app.root.ids.add_walk_screen.ids.path_img.text = self.path_img
               self.app.root.ids.add_walk_screen.ids.img.opacity = 1
          if self.app.root.current == 'data_personal':
               self.app.root.ids.personal_data.ids.profile_icon.icon = self.path_img
          self.dismiss()
class Lost_card(RoundedRectangularElevationBehavior,MDCard):
     def delete_ad(self,card):
          global current_user
          self.app = MDApp.get_running_app()
          self.select_card = card.parent.parent.parent.ids.ids.date.text
          query(f'DELETE FROM COMMENT WHERE (ID_PROFILE = {current_user}) AND (ID_AD = (SELECT ID FROM AD WHERE CREATE_DATE = "{self.select_card}")) ','delete')
          query(f'DELETE FROM AD WHERE CREATE_DATE = "{self.select_card}"','delete')
          self.app.root.ids.profile_screen.download_my_ad()
     def change(self):
          global current_user
          self.app = MDApp.get_running_app()
          query(f'UPDATE AD SET ','delete')
          self.app.root.ids.profile_screen.download_my_ad()
          self.app.root.current = 'my_ad'
class Service_card(RoundedRectangularElevationBehavior,MDCard):
     def delete_service(self,card):
          global current_user
          self.app = MDApp.get_running_app()
          self.select_card = card.parent.parent.parent.ids.date.text
          query(f'DELETE FROM REVIEW WHERE (ID_PROFILE = {current_user}) AND (ID_AD = (SELECT ID FROM AD WHERE CREATE_DATE = "{self.select_card}")) ','delete')
          query(f'DELETE FROM SERVICE WHERE CREATE_DATE = "{self.select_card}"','delete')
          self.app.root.ids.profile_screen.download_my_service()
class Notification_Card(RoundedRectangularElevationBehavior,MDCard):
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
class Reviews_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Comment_card(RoundedRectangularElevationBehavior,MDCard):
     pass
class Tab(MDFloatLayout, MDTabsBase):
     pass
class Lost_list(Tab):
     pass
class Lost_map(Tab):
     pass
class Sign_in(Tab):
     def show_dialog(self,text):
          self.dialog = MDDialog(title='????????????',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='????',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
          self.dialog.dismiss(force=True)
     def on_location(self, **kwargs):
          #self.lat = kwargs['lat']
          #self.lon = kwargs['lon']
          self.marker = MapMarker()
          self.marker.lat = 55.57255244187822#self.lat
          self.marker.lon = 42.03819546003002#self.lon
          self.marker.source = r'Image\me_marker.png'
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.lat = 55.57255244187822#self.lat
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.lon = 42.03819546003002#self.lon
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.add_marker(self.marker)
     def gps_locate(self):
          gps.configure(on_location=self.on_location)
          gps.start(1000, 0)
     def add_markers(self):
          # request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
          self.app = MDApp.get_running_app()
          self.count = query(f'SELECT COUNT(*) FROM AD','select')
          self.answer = query(f'SELECT * FROM AD ORDER BY ID DESC','select','all')
          self.on_location()
          for i in range(self.count):
          #for i in range(1):
               self.marker = MapMarkerPopup()
               self.marker_popup = PopupMarker()
               self.marker_popup.size_hint = None,None
               self.marker_popup.size = 250,250
               self.marker_popup.ids.type_marker.text = query(f'SELECT NAME FROM TYPE_AD WHERE ID = (SELECT TYPE FROM AD WHERE ID = {self.answer[i][0]})','select')
               self.bdata = query(f'SELECT PHOTO FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.data = io.BytesIO(self.bdata)
               self.marker_popup.ids.img_marker.texture = CoreImage(self.data, ext = "png").texture
               self.lat = query(f'SELECT LAT FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.lon = query(f'SELECT LON FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.marker.lat = self.lat
               self.marker.lon = self.lon
               self.marker.source = r'Image\marker.png'
               self.marker.add_widget(self.marker_popup)
               self.app.root.ids.mainscreen.ids.lost_map.ids.map.add_marker(self.marker)
     def get_text_sign(self):
          self.email = self.ids.email_sign.text
          self.password = self.ids.passw_sign.text
          self.app = MDApp.get_running_app()
          self.answer = query(f'SELECT EMAIL FROM PROFILE WHERE EMAIL = "{self.email}"','select')
          self.salt = query(f'SELECT SALT FROM PROFILE WHERE EMAIL = "{self.email}"','select')
          self.password_db = query(f'SELECT PASSWORD FROM PROFILE WHERE EMAIL = "{self.email}"','select')
          self.hash = hashlib.sha512(bytes(self.password,encoding='utf-8')+bytes(self.salt,encoding='utf-8'))
          self.hash_dig = self.hash.hexdigest()
          if self.answer == None:
               self.show_dialog('???????????? ?????????????? ???????????? ???? ????????????????????')
          if self.hash_dig != self.password_db:
               self.show_dialog('???????????? ???? ????????????')
          elif self.email == self.answer and self.hash_dig == self.password_db:
               global current_user
               current_user = query(f'SELECT ID FROM PROFILE WHERE EMAIL = "{self.email}"','select')
               self.app.root.current = "main"
               self.app.root.transition.direction = "left"
          
class Registration(Tab):
     hint = StringProperty('??????')
     def show_dialog(self,text):
          self.dialog = MDDialog(title='????????????',
                              text=text, size_hint=(0.5, 0.2),
                              buttons=[MDFlatButton(text='????',on_release = self.dialog_close)]
                              )
          self.dialog.open()
     def dialog_close(self,obj):
        self.dialog.dismiss(force=True)
     def on_location(self, **kwargs):
          #self.lat = kwargs['lat']
          #self.lon = kwargs['lon']
          self.marker = MapMarker()
          self.marker.lat = 55.57255244187822#self.lat
          self.marker.lon = 42.03819546003002#self.lon
          self.marker.source = r'Image\me_marker.png'
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.lat = 55.57255244187822#self.lat
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.lon = 42.03819546003002#self.lon
          self.app.root.ids.mainscreen.ids.lost_map.ids.map.add_marker(self.marker)
     def gps_locate(self):
          gps.configure(on_location=self.on_location)
          gps.start(1000, 0)
     def add_markers(self):
          # request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])
          self.app = MDApp.get_running_app()
          self.count = query(f'SELECT COUNT(*) FROM AD','select')
          self.answer = query(f'SELECT * FROM AD ORDER BY ID DESC','select','all')
          self.on_location()
          for i in range(self.count):
          #for i in range(1):
               self.marker = MapMarkerPopup()
               self.marker_popup = PopupMarker()
               self.marker_popup.size_hint = None,None
               self.marker_popup.size = 250,250
               self.marker_popup.ids.type_marker.text = query(f'SELECT NAME FROM TYPE_AD WHERE ID = (SELECT TYPE FROM AD WHERE ID = {self.answer[i][0]})','select')
               self.bdata = query(f'SELECT PHOTO FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.data = io.BytesIO(self.bdata)
               self.marker_popup.ids.img_marker.texture = CoreImage(self.data, ext = "png").texture
               self.lat = query(f'SELECT LAT FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.lon = query(f'SELECT LON FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.marker.lat = self.lat
               self.marker.lon = self.lon
               self.marker.source = r'Image\marker.png'
               self.marker.add_widget(self.marker_popup)
               self.app.root.ids.mainscreen.ids.lost_map.ids.map.add_marker(self.marker)
     def check_text(self,instance, value, err=[]):
          self.app = MDApp.get_running_app()
          if self.app.root.current == 'login':
               for k, v in self.ids.items():
                    if v == instance:
                         if k == 'name_reg':
                              match_name = re.fullmatch(r'^[??-????-??????a-zA-Z]+$', rf'{value}')
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
                              match_lname = re.fullmatch(r'^[??-????-??????a-zA-Z]+$', rf'{value}')
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
          phone = self.ids.phone_reg.text
          password1 = self.ids.passw_reg1.text
          password2 = self.ids.passw_reg2.text
          for i in self.ids.keys():
               if i.find('reg') != -1:
                    if not self.ids[i].text:
                         if i not in empty:
                              empty.remove(i)
                         self.show_dialog('???? ?????? ???????? ??????????????????')
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
          self.app = MDApp.get_running_app()
          self.fname = self.ids.name_reg.text
          self.lname = self.ids.lname_reg.text
          self.email = self.ids.email_reg.text
          #city = self.ids.city_reg.text
          self.phone = self.ids.phone_reg.text
          self.password = self.ids.passw_reg1.text
          self.salt_b = os.urandom(len(self.password)*2)
          self.dec_salt = self.salt_b.decode('utf-8',errors='ignore')
          #print(bytes(dec_salt,encoding='utf-8'))
          #print(password+bytes(dec_salt,encoding='utf-8'))
          self.hash = hashlib.sha512(bytes(self.password,encoding='utf-8')+bytes(self.dec_salt,encoding='utf-8'))
          self.hex_dig = self.hash.hexdigest()
          #print(hex_dig)
          #query(f'INSERT INTO city VALUE({city})','insert')
          with open('Image\\def_img_profile.png', 'rb') as file:
               self.blobData = file.read()
          query(f'INSERT INTO profile (FIRST_NAME, LAST_NAME, AVATAR, EMAIL, PHONE_NUMBER, PASSWORD, SALT) VALUES ("{self.fname}","{self.lname}",%s,"{self.email}","{self.phone}","{self.hex_dig}","{self.dec_salt}")','insert',photo=self.blobData)
          global current_user
          current_user = query(f'SELECT ID FROM PROFILE WHERE EMAIL = "{self.email}"','select')
          self.app.root.current = "main"
          self.app.root.transition.direction = "left"
class About_me(Tab):
     pass
class PopupMarker(Widget):
     pass
class Ad(RelativeLayout):
     name = StringProperty('??????')
class NavigationBar(FakeRectangularElevationBehavior,MDFloatLayout):
     pass

 
class PetsApp(MDApp):
     def check_internet(self):
          try:
               request = requests.get('https://www.google.com/', timeout=10)
               return True
          except (requests.ConnectionError, requests.Timeout) as exception:
               self.dialog = MDDialog(title='????????????',
                                   text='?????????????????????? ?????????????????????? ?? ??????????????????', size_hint=(0.5, 0.2),
                                   buttons=[MDFlatButton(text='????', on_release=self.close_dialog)]
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
                              self.root.get_screen('notification').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('notif_noreg').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
                              self.root.get_screen('notification').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
               if 'nav_icon5' == current_id:
                    for i in range(5):
                         if f'nav_icon{i+1}' == current_id:
                              self.root.get_screen('profile').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                              self.root.get_screen('profile_noreg').ids[f'nav_icon{i+1}'].text_color = 0.34,0.71,0.98,1
                         else:
                              self.root.get_screen('profile').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
                              self.root.get_screen('profile_noreg').ids[f'nav_icon{i+1}'].text_color = 0,0,0,1
     def transition_notif(self):
          global current_user
          if current_user == None:
               self.root.current = 'notif_noreg'
          else:
               self.root.current = 'notification'
     def transition_profile(self):
          global current_user
          if current_user == None:
               self.root.current = 'profile_noreg'
          else:
               self.root.current = 'profile'
     def removeall_ad(self):
        rows = [i for i in self.root.ids.mainscreen.ids.lost_list.ids.container_lost.children]
        for row1 in rows:
            if isinstance(row1, MDCard):
                self.root.ids.mainscreen.ids.lost_list.ids.container_lost.remove_widget(row1)
     def removeall_service(self):
        rows = [i for i in self.root.ids.service_list_screen.ids.container_service.children]
        for row1 in rows:
            if isinstance(row1, MDCard):
                self.root.ids.service_list_screen.ids.container_service.remove_widget(row1)
     def add_cards_ads(self):
          global current_user
          self.count = query(f'SELECT COUNT(*) FROM AD','select')
          self.answer = query('SELECT * FROM AD ORDER BY ID DESC','select','all')
          self.removeall_ad()
          for i in range(self.count):
               self.card = Lost_card()
               self.bdata = query(f'SELECT PHOTO FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.data = io.BytesIO(self.bdata)
               self.card.ids.card_image.texture = CoreImage(self.data, ext = "png").texture
               self.date = query(f'SELECT CREATE_DATE FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.gender = query(f'SELECT GENDER FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.type = query(f'SELECT TYPE FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.city = query(f'SELECT CITY FROM AD WHERE ID = {self.answer[i][0]}','select')
               self.card.ids.date.text = str(self.date)
               self.card.ids.card_date.text = self.date.strftime('%d %B %Y, %H:%M')
               self.card.ids.gender.text = self.gender
               if self.type == 1 and self.gender == '??????????????':
                    self.card.ids.type.text = '????????????'
               elif self.type == 1 and self.gender == '??????????????':
                    self.card.ids.type.text = '??????????????'
               if self.type == 2 and self.gender == '??????????????':
                    self.card.ids.type.text = '??????????????'
               elif self.type == 2 and self.gender == '??????????????':
                    self.card.ids.type.text = '????????????????'
               self.card.ids.city.text = self.city
               self.card.bind(on_release=self.display_ad)
               self.root.ids.mainscreen.ids.lost_list.ids.container_lost.add_widget(self.card)
     def add_cards_services(self):
          global current_user
          self.count = query(f'SELECT COUNT(*) FROM SERVICE','select')
          self.answer = query('SELECT * FROM SERVICE ORDER BY ID DESC','select','all')
          self.removeall_service()
          for i in range(self.count):
          #for i in range(1):
               self.card = Service_card()
               self.create_date = query(f'SELECT CREATE_DATE FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
               self.bdata = query(f'SELECT PHOTO FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
               self.data = io.BytesIO(self.bdata)
               self.card.ids.card_image.texture = CoreImage(self.data, ext = "png").texture
               self.fname = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.answer[i][0]})','select')
               self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE ID = {self.answer[i][0]})','select')
               self.city = query(f'SELECT CITY FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
               self.kind = query(f'SELECT NAME FROM KIND_SERVICE WHERE ID = (SELECT KIND FROM SERVICE WHERE ID = {self.answer[i][0]})','select')
               self.price = query(f'SELECT PRICE FROM SERVICE WHERE ID = {self.answer[i][0]}','select')
               self.card.ids.name_service_card.text = self.fname + ' ' + self.lname
               self.card.ids.city_service_card.text = self.city
               self.card.ids.kind_service_card.text = self.kind
               if self.kind == '????????????????????':
                    self.card.ids.price_service_card.text = self.price+' ????????????/??????????'
               if self.kind == '????????':
                    self.card.ids.price_service_card.text = self.price+' ????????????/??????????'
               if self.kind == '??????????':
                    self.card.ids.price_service_card.text = self.price+' ????????????/30 ??????????'
               self.card.ids.date_service_card.text = self.create_date.strftime('%d %B %Y, %H:%M')
               self.card.bind(on_release=self.display_service)
               self.root.ids.service_list_screen.ids.container_service.add_widget(self.card)
     def display_ad(self,card):
          self.create_date = card.ids.date.text
          self.bdata = query(f'SELECT PHOTO FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.data = io.BytesIO(self.bdata)
          self.root.ids.ad_screen.ids.ad_container.ids.ad_image.texture = CoreImage(self.data, ext = "png").texture
          self.lat = query(f'SELECT LAT FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.lon = query(f'SELECT LON FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.kind = query(f'SELECT NAME FROM KIND_PET WHERE ID = (SELECT KIND_PETS FROM AD WHERE CREATE_DATE = "{self.create_date}")','select')
          self.gender = query(f'SELECT GENDER FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.comment = query(f'SELECT TEXT FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.fname = query(f'SELECT FIRST_NAME FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.phone_number = query(f'SELECT PHONE_NUMBER FROM AD WHERE CREATE_DATE = "{self.create_date}"','select')
          self.root.ids.ad_screen.ids.ad_container.ids.ad_date.text = self.create_date
          self.root.ids.ad_screen.ids.ad_container.ids.ad_map.lat = self.lat
          self.root.ids.ad_screen.ids.ad_container.ids.ad_map.lon = self.lon
          self.root.ids.ad_screen.ids.ad_container.ids.ad_mapmarker.lat = self.lat
          self.root.ids.ad_screen.ids.ad_container.ids.ad_mapmarker.lon = self.lon
          self.root.ids.ad_screen.ids.ad_container.ids.ad_kind.text = self.kind
          self.root.ids.ad_screen.ids.ad_container.ids.ad_gender.text = self.gender
          self.root.ids.ad_screen.ids.ad_container.ids.ad_text.text = self.comment
          self.root.ids.ad_screen.ids.ad_container.ids.ad_name.text = self.fname
          self.root.ids.ad_screen.ids.ad_container.ids.ad_phone.text = self.phone_number
          self.root.current = 'ad'
     def display_service(self, card):
          self.create_date = card.ids.date.text
          self.bdata = query(f'SELECT PHOTO FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
          self.data = io.BytesIO(self.bdata)
          self.root.ids.service_screen.ids.service_image.texture = CoreImage(self.data, ext = "png").texture
          self.fname = query(f'SELECT FIRST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
          self.lname = query(f'SELECT LAST_NAME FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
          self.address = query(f'SELECT ADDRESS FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
          self.kind = query(f'SELECT NAME FROM KIND_SERVICE WHERE ID = (SELECT KIND FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
          self.price = query(f'SELECT PRICE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
          
          self.root.ids.service_screen.ids.name_service.text = self.fname + ' ' + self.lname
          self.root.ids.service_screen.ids.address_service.text = self.address
          self.root.ids.service_screen.ids.kind_service.text = self.kind
          if self.kind == '??????????':
               self.card.ids.type_price.text = '?????????????????? ???? 30 ??????????:'
          self.root.ids.service_screen.ids.price_service.text = self.price + ' ????????????'
          self.root.ids.service_screen.ids.date_service.text = self.create_date
          
          self.kind_pet = query(f'SELECT NAME FROM KIND_PET WHERE ID = (SELECT KIND_PETS FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
          self.age = query(f'SELECT AGE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
          self.phone_number = query(f'SELECT PHONE_NUMBER FROM PROFILE WHERE ID = (SELECT ID_PROFILE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}")','select')
          self.comment = query(f'SELECT ABOUT_ME FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
          if self.kind_pet == '????????????' or self.kind_pet == '??????':
               self.size_dog = query(f'SELECT SIZE_DOG FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.root.ids.service_screen.ids.size_dog2_serv.text = self.size_dog
               self.root.ids.service_screen.ids.age_serv.text = self.age
               self.root.ids.service_screen.ids.phone_serv.text = self.phone_number
               self.root.ids.service_screen.ids.comment.text = self.comment
               self.medicine = query(f'SELECT MEDICINE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.injection = query(f'SELECT INJECTION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.control = query(f'SELECT CONTROL FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.education = query(f'SELECT EDUCATION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select') 
               if not self.medicine:
                    self.root.ids.service_screen.ids.medicine.disabled = True
               if not self.injection:
                    self.root.ids.service_screen.ids.injection.disabled = True
               if not self.control:
                    self.root.ids.service_screen.ids.control.disabled = True
               if not self.education:
                    self.root.ids.service_screen.ids.education.disabled = True
               else:
                    self.name_educ = query(f'SELECT NAME_EDUCATION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select') 
                    self.root.ids.service_screen.ids.education.text = '- ???????????????????? ?????????????????????? - '+ self.name_educ
               self.root.current = 'service'
          if self.kind_pet == '??????????':
               self.root.ids.service_screen.ids.size_dog1_serv.disabled = True
               self.root.ids.service_screen.ids.size_dog2_serv.disabled = True
               self.root.ids.service_screen.ids.age_serv.text = self.age
               self.root.ids.service_screen.ids.phone_serv.text = self.phone_number
               self.root.ids.service_screen.ids.comment.text = self.comment
               self.medicine = query(f'SELECT MEDICINE FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.injection = query(f'SELECT INJECTION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.control = query(f'SELECT CONTROL FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select')
               self.education = query(f'SELECT EDUCATION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select') 
               if not self.medicine:
                    self.root.ids.service_screen.ids.medicine.disabled = True
               if not self.injection:
                    self.root.ids.service_screen.ids.injection.disabled = True
               if not self.control:
                    self.root.ids.service_screen.ids.control.disabled = True
               if not self.education:
                    self.root.ids.service_screen.ids.education.disabled = True
               else:
                    self.name_educ = query(f'SELECT NAME_EDUCATION FROM SERVICE WHERE CREATE_DATE = "{self.create_date}"','select') 
                    self.root.ids.service_screen.ids.education.text = '- ???????????????????? ?????????????????????? - '+ self.name_educ
               self.root.current = 'service'
               
     def on_start(self, **kwargs):
          self.check_internet()
          self.add_cards_ads()
          self.add_cards_services()
#kv = Builder.load_file("pets.kv")
if __name__ == '__main__':
     PetsApp().run()