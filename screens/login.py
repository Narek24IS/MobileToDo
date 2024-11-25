from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from screens.base import CustomScreen


class LoginScreen(CustomScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.username = MDTextField(hint_text="Username", size_hint_x=0.8, pos_hint={"center_x": 0.5})
        self.password = MDTextField(hint_text="Password", password=True, size_hint_x=0.8, pos_hint={"center_x": 0.5})
        self.message = MDLabel(halign="center", theme_text_color="ContrastParentBackground", font_style="H5")

        login_button = MDRaisedButton(text='Login', pos_hint={"center_x": 0.5})
        login_button.bind(on_press=self.login)

        register_button = MDRaisedButton(text='Go to Register', pos_hint={"center_x": 0.5})
        register_button.bind(on_press=self.get_screen_switcher('register'))

        self.layout.add_widget(self.username)
        self.layout.add_widget(self.password)
        self.layout.add_widget(self.message)
        self.layout.add_widget(login_button)
        self.layout.add_widget(register_button)

        self.add_widget(self.layout)

    def login(self, instance):
        self.cursor.execute('SELECT * FROM users WHERE username=? AND password=?',
                            (self.username.text, self.password.text))
        user = self.cursor.fetchone()

        if user:
            self.manager.current_user_id = user[0]
            self.get_screen_switcher('shopping_list')()
        else:
            self.message.text = 'Invalid credentials'
