from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from screens.base import CustomScreen


class ShoppingListScreen(CustomScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout.center_y = 50
        self.item_input = MDTextField(hint_text='Enter item', multiline=False)
        self.price_input = MDTextField(hint_text='Enter price', multiline=False, input_filter='float')
        self.message = MDLabel(
            halign="center",
            theme_text_color="ContrastParentBackground",
            font_style="H5",
        )

        scroll_view = MDScrollView(size_hint_min_y=200)
        self.item_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.item_list.bind(minimum_height=self.item_list.setter('height'))
        scroll_view.add_widget(self.item_list)

        add_button = MDRaisedButton(text='Add Item', pos_hint={"center_x": 0.5})
        add_button.bind(on_press=self.add_item)

        self.layout.add_widget(self.item_input)
        self.layout.add_widget(self.price_input)
        self.layout.add_widget(add_button)
        self.layout.add_widget(scroll_view)
        self.layout.add_widget(self.message)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.user_id = self.manager.current_user_id
        self.update_item_list()

    def add_item(self, instance):
        item_name = self.item_input.text
        price = self.price_input.text

        if item_name:
            self.cursor.execute('INSERT INTO shopping_list (item, price, purchased, user_id) VALUES (?, ?, ?, ?)',
                                (item_name, float(price) if price else 0.0, 0, self.user_id))
            self.conn.commit()

            self.item_input.text = ''
            self.price_input.text = ''
            self.update_item_list()
        else:
            self.message.text = 'Item name cannot be empty.'

    def update_item_list(self):
        self.item_list.clear_widgets()
        self.cursor.execute('SELECT id, item, price, purchased FROM shopping_list WHERE user_id = ?', (self.user_id,))
        items = self.cursor.fetchall()

        for item_id, item_name, price, purchased in items:
            item_layout = BoxLayout(size_hint_y=None, height=40, padding=10, spacing=10)

            checkbox = MDCheckbox(active=bool(purchased))
            checkbox.bind(active=self.toggle_purchased(item_id))

            label = MDLabel(text=f"{item_id} {item_name} - ${price}", size_hint_x=1,
                            halign="left",
                            theme_text_color="Primary",
                            font_style="H6",
                            )

            edit_button = MDRaisedButton(text='Edit', size_hint_x=0.2, pos_hint={"center_x": 0.5})
            edit_button.bind(on_press=self.edit_item(item_id))

            delete_button = MDRaisedButton(text='Delete', size_hint_x=0.2, pos_hint={"center_x": 0.5})
            delete_button.bind(on_press=self.delete_item(item_id))

            item_layout.add_widget(checkbox)
            item_layout.add_widget(label)
            item_layout.add_widget(edit_button)
            item_layout.add_widget(delete_button)

            self.item_list.add_widget(item_layout)

        self.update_total()

    def toggle_purchased(self, item_id):
        def inner(instance=None, active=False):
            self.cursor.execute('UPDATE shopping_list SET purchased = ? WHERE id = ?',
                                (int(active), item_id))
            self.conn.commit()
            self.update_item_list()

        return inner

    def edit_item(self, item_id):
        def inner(instance=None):
            self.cursor.execute('SELECT item, price FROM shopping_list WHERE id = ?', (item_id,))
            item = self.cursor.fetchone()

            if item:
                self.item_input.text = item[0]
                self.price_input.text = str(item[1])

                self.delete_item(item_id)(instance)

        return inner

    def delete_item(self, item_id):
        def inner(instance=None):
            self.cursor.execute('DELETE FROM shopping_list WHERE id = ?', (item_id,))
            self.conn.commit()
            self.update_item_list()

        return inner

    def update_total(self):
        self.cursor.execute('SELECT SUM(price) FROM shopping_list WHERE purchased = 1 AND user_id = ?', (self.user_id,))
        total = self.cursor.fetchone()[0] or 0.0

        self.message.text = f'Total Purchased: ${total:.2f}'
