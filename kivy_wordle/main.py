import random
from pathlib import Path
from typing import Final

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

GREEN_COLOR: Final[str] = "03fc1c"
YELLOW_COLOR: Final[str] = "fcc603"


class LimitedTextInput(TextInput):
    max_length = 5

    def __init__(self, possible_characters: set[str] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.possible_characters: set[str] = set() if possible_characters is None else possible_characters

    def insert_text(self, substring: str, from_undo=False) -> None:
        if len(self.text) >= self.max_length:
            return
        if substring not in self.possible_characters:
            return
        TextInput.insert_text(self, substring, from_undo)


def _get_word_list() -> list[str]:
    words_file_path = Path(__file__).parent / "cz_words_5.txt"
    return [x.lower() for x in words_file_path.read_text(encoding='utf-8').strip().splitlines()]


class WordleLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.word_list: list[str] = _get_word_list()
        self.secret_word = random.choice(self.word_list)
        self.max_attempts = 5
        self.current_attempt = 0

        self.result_label = self.ids.result_label
        self.words_label = self.ids.words_label
        self.submit_button = self.ids.submit_button
        self.input_box = self.ids.input_box

        possible_characters = {letter for word in self.word_list for letter in word}
        self.input_box.possible_characters = possible_characters
        self.words_label.text = "  ".join(sorted(possible_characters))

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

        # Display result of the guess
        if not self.result_label.text:
            self.result_label.text += f"Attempt {self.current_attempt}: {result}"
        else:
            self.result_label.text += f"\nAttempt {self.current_attempt}: {result}"

        if guess == self.secret_word:
            self.result_label.text += f"\n\n[size=20]Congratulations! You guessed the word: [b]{self.secret_word}[/b][/size]"
            self.input_box.disabled = True
            return

        if self.current_attempt >= self.max_attempts:
            self.result_label.text += f"\n\n[size=20]You lost! The word was: [b]{self.secret_word}[/b][/size]"
            self.input_box.disabled = True
            return

    def color_letter(self, letter: str, color: str) -> None:
        if color == GREEN_COLOR and f"{YELLOW_COLOR}]{letter}" in self.words_label.text:
            self.words_label.text = self.words_label.text.replace(f"{YELLOW_COLOR}]{letter}", f"{color}]{letter}")
            return

        if f"{letter}  " not in self.words_label.text and f"  {letter}" not in self.words_label.text:
            return

        text = self.words_label.text
        def get_index(pattern: str)-> int:
            try:
                return text.index(pattern)
            except ValueError:
                return 0

        index = max(get_index(f"{letter}  "), get_index(f"  {letter}"))
        self.words_label.text = text[:index] + f"[color=#{color}]{letter}[/color]" + text[index + 1:]

    def remove_letter(self, letter: str) -> None:
        self.words_label.text = self.words_label.text.replace(f"{letter}  ", "").replace(f"  {letter}", "")

    def evaluate_guess(self, guess: str) -> str:
        result = ""
        for i, letter in enumerate(guess):
            if letter == self.secret_word[i]:
                color = GREEN_COLOR
                result += f"[color=#{color}]{letter}[/color]"  # Correct letter in correct position
                self.color_letter(letter, color)
            elif letter in self.secret_word:
                color = YELLOW_COLOR
                result += f"[color=#{color}]{letter}[/color]"  # Correct letter in wrong position
                self.color_letter(letter, color)
            else:
                result += f"[color=#fc0303]{letter}[/color]"  # Incorrect letter
                self.remove_letter(letter)

        return f"[b]{result}[/b]"

    def show_popup(self, title: str, message: str) -> None:
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class WordleApp(App):

    def build(self):
        return WordleLayout()


if __name__ == "__main__":
    WordleApp().run()
