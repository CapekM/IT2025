import kivy
from kivy.uix.gridlayout import GridLayout

kivy.require("2.3.1")

from kivy.uix.button import Button, Label
from kivy.uix.boxlayout import BoxLayout

from kivy.app import App


class Calculator_layout(BoxLayout):

    def __init__(self, **kwargs):
        super(Calculator_layout, self).__init__(**kwargs, orientation = "vertical")

        self.result_label = Label(size_hint_y=0.75, font_size=50)
        self.add_widget(self.result_label)

        buttons_symbols = (
            "1", "2", "3", "+",
            "4", "5", "6", "-",
            "7", "8", "9", ".",
            "0", "*", "/", "=",
        )
        button_grid = GridLayout(cols=4, size_hint_y=2)
        for symbol in buttons_symbols:
            button_grid.add_widget(Button(text=symbol))

        button_grid.children[0].bind(on_press=self.evaluate)
        for button in button_grid.children[1:]:
            button.bind(on_press=self.add_text)

        self.add_widget(button_grid)

        clear_button = Button(text="Clear", size_hint_y=None, height=100, on_press=self.clear)
        self.add_widget(clear_button)

    def add_text(self, button_instance):
        self.result_label.text += button_instance.text

    def evaluate(self, button_instance):
        try:
            self.result_label.text = str(eval(self.result_label.text))
        except SyntaxError:
            self.result_label.text = "SyntaxError"

    def clear(self, button_instance):
        self.result_label.text = ""


class MainApp(App):
    def build(self):
        return Calculator_layout()


if __name__ == '__main__':
    MainApp().run()
