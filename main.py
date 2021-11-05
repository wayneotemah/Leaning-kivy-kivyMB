from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import MDList, IconLeftWidget, TwoLineIconListItem
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore

import urllib

Window.size = (300, 552)
store = JsonStore(filename='test.json')


class AppScreen(MDScreen):
    def on_enter(self):
        def success(req, result):
            print(result)
            for student in result.items():
                item = TwoLineIconListItem(text=student[1]['admin'], secondary_text=student[1]['email'])
                icons = IconLeftWidget(icon="android")
                item.add_widget(icons)
                self.ids.contact_list.add_widget(item)
                # print(student)

        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}

        req = UrlRequest('http://127.0.0.1:5000/get_students', on_success=success, req_headers=headers)


class EventScreen(MDScreen):
    pass


class HomeScreen(MDScreen):
    pass


class CommunityScreen(MDScreen):
    pass


class ProfileScreen(MDScreen):
    pass


class MainScreen(MDScreen):
    # main intro login screen
    pass


class LoginScreen(MDScreen):
    def ditaLogin(self, adimn, pw):
        def posted(req, result):
            store.put('Auth', token=result['token'])
            self.manager.current = 'AppScreen'

        params = urllib.parse.urlencode({'admin': adimn.text, 'password': pw.text})
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}
        req = UrlRequest('http://127.0.0.1:5000/login', on_success=posted, req_body=params,
                         req_headers=headers)


class SignupScreen(MDScreen):
    def ditasignup(self, adimn, pw, email):
        def posted(req, result):
            self.manager.current = 'login'

        params = urllib.parse.urlencode({'admin': adimn.text, 'password': pw.text, 'email': email.text})
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}
        req = UrlRequest('http://127.0.0.1:5000/signup', on_success=posted, req_body=params,
                         req_headers=headers)


class DitaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"

        self.sm = ScreenManager()
        self.sm.add_widget(AppScreen(name='AppScreen'))
        self.sm.add_widget(CommunityScreen(name='CommunityScreen'))
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(ProfileScreen(name='ProfileScreen'))
        self.sm.add_widget(HomeScreen(name='HomeScreen'))
        self.sm.add_widget(ProfileScreen(name='EventScreen'))
        self.sm.add_widget(SignupScreen(name='signup'))


        return self.sm

    def change_screen(self, screen):
        self.sm.current = screen


if __name__ == "__main__":
    DitaApp().run()
