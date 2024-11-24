from kivy.uix.screenmanager import ScreenManager
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.shopping_list import ShoppingListScreen
from kivymd.app import MDApp
from database import initialize_db

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen(name='login'))
        self.add_widget(RegisterScreen(name='register'))
        self.add_widget(ShoppingListScreen(name='shopping_list'))

class MainApp(MDApp):
    def build(self):
        initialize_db()
        return ScreenManagement()

if __name__ == '__main__':
    MainApp().run()
