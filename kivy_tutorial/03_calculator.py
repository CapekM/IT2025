import kivy

kivy.require("2.3.1")

from kivy.uix.button import Button, Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from kivy.app import App


class Calculator_layout(BoxLayout):

    def __init__(self, **kwargs):
        super(Calculator_layout, self).__init__(**kwargs)
        self.orientation = "vertical"

        widget = BoxLayout(orientation="horizontal")
        self.number1_input = TextInput(multiline=False)
        self.combobox = Spinner(text="+", values=("+", "-", "*", "/"))
        self.number2_input = TextInput(multiline=False)
        self.result_label = Label(text="0")
        widget.add_widget(self.number1_input)
        widget.add_widget(self.combobox)
        widget.add_widget(self.number2_input)
        widget.add_widget(self.result_label)
        self.add_widget(widget)

        self.button = Button(text="=", on_press=self.evaluate)
        self.add_widget(self.button)

    def evaluate(self, button_instance):
        if self.number1_input.text == "" or self.number2_input.text == "":
            return None
        if self.combobox.text == "+":
            result = float(self.number1_input.text) + float(self.number2_input.text)
        elif self.combobox.text == "-":
            result = float(self.number1_input.text) - float(self.number2_input.text)
        elif self.combobox.text == "*":
            result = float(self.number1_input.text) * float(self.number2_input.text)
        elif self.combobox.text == "/":
            if self.number2_input.text == "0":
                self.result_label.text = "ERROR"
                return None
            result = float(self.number1_input.text) / float(self.number2_input.text)
        else:
            raise ValueError(f"Unknown {self.combobox.text = }")

        self.result_label.text = str(result)


class MainApp(App):
    def build(self):
        return Calculator_layout()


if __name__ == '__main__':
    MainApp().run()
