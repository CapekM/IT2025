from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class WordleLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(WordleLayout, self).__init__(**kwargs, orientation="vertical")
        self.word_list: list[str] = ["apple", "melon"]  # TODO better word list
        self.secret_word = "peach"  # random.choice(self.word_list)
        self.max_attempts = 5
        self.current_attempt = 0

        self.input_box = TextInput(multiline=False, hint_text="Enter your guess (5 letters)")  # TODO length 5
        self.add_widget(self.input_box)

        self.submit_button = Button(text="Submit Guess")
        self.submit_button.bind(on_press=self.check_guess)
        self.add_widget(self.submit_button)

        self.result_label = Label(text="", size_hint_y=None, height=40, markup=True)
        # https://kivy.org/doc/stable/api-kivy.core.text.markup.html
        self.add_widget(self.result_label)

    def check_guess(self, instance) -> None:
        guess = self.input_box.text.lower()
        if len(guess) != 5:
            self.show_popup("Invalid Guess", "Please enter a 5-letter word.")
            return

        if guess not in self.word_list:
            self.show_popup("Invalid Word", "This word is not in the list.")
            return

        self.current_attempt += 1
        result = self.evaluate_guess(guess)

        if guess == self.secret_word:
            self.result_label.text = f"Congratulations! You guessed the word: [b]{self.secret_word}[/b]"
            self.input_box.disabled = True
            return

        if self.current_attempt >= self.max_attempts:
            self.result_label.text = f"You lost! The word was: [b]{self.secret_word}[/b]"
            self.input_box.disabled = True
            return

        # Display result of the guess
        self.result_label.text = f"Attempt {self.current_attempt}: {result}"
        # TODO attempts history

    def evaluate_guess(self, guess: str) -> str:
        result = ""
        for i, letter in enumerate(guess):
            if letter == self.secret_word[i]:
                result += f"[color=#03fc1c]{letter}[/color]"  # Correct letter in correct position
            elif letter in self.secret_word:
                result += f"[color=#fcc603]{letter}[/color]"  # Correct letter in wrong position
            else:
                result += f"[color=#fc0303]{letter}[/color]"  # Incorrect letter
        return f"[b]{result}[/b]"

    def show_popup(self, title: str, message: str) -> None:
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class WordleApp(App):

    def build(self):
        return WordleLayout()


if __name__ == "__main__":
    WordleApp().run()
