from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
import sqlite3

USER_ID=0

class CustomScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_max_y=300, center_y=200)
        self.conn = sqlite3.connect('app.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_screen_switcher(self, screen_name):
        def inner(instance=None):
            self.manager.current = screen_name

        return inner