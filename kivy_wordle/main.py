import random
from pathlib import Path
from typing import Final

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

GREEN_COLOR: Final[str] = "03fc1c"
YELLOW_COLOR: Final[str] = "fcc603"
BLACK_COLOR: Final[str] = "000000"


def _get_word_list() -> list[str]:
    words_file_path = Path(__file__).parent / "cz_words_5.txt"
    return [x.upper() for x in words_file_path.read_text(encoding='utf-8').strip().splitlines()]


class KeyboardButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = "FFFFFF"

class WordleLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.word_list: list[str] = _get_word_list()
        self.secret_word = random.choice(self.word_list)
        self.words_len = 5
        self.max_attempts = 5
        self.current_attempt = 0

        self.result_label = self.ids.result_label
        self.words_label = self.ids.words_label
        self.submit_button = self.ids.submit_button
        self.keyboard_layout = self.ids.keyboard_layout

        self.words_label.text = "LÁSKA"  # TODO delete, it is for debugging purposes

        keyboard_layout = [
            ['Ú/Ů', 'Č', 'Ě', 'Ř', 'Š', 'Ž'],
            ['W', 'E/É', 'R', 'T/Ť', 'Y/Ý', 'U', 'I/Í', 'O/Ó', 'P'],
            ['A/Á', 'S', 'D/Ď', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'M', 'N/Ň', '<-'],
        ]
        for row in keyboard_layout:
            keyboard_row_layout = BoxLayout()
            for key in row:
                button = KeyboardButton(text=key, on_press=self.on_key_press)
                print(f"{button.text = } {button.pos = } {button.size = } {button.x = } {button.y = }")
                keyboard_row_layout.add_widget(button)
            for b in keyboard_row_layout.children:
                # print(f"{dir(b) = }")
                print(f"{b.text = } {b.pos = } {b.size = } {b.x = } {b.y = }")
            print()
            self.keyboard_layout.add_widget(keyboard_row_layout)

    def on_key_press(self, button):
        if button.text == '<-':
            if len(self.words_label.text):
                self.words_label.text = self.words_label.text[:-1]
        elif len(self.words_label.text) < self.words_len:
            if "/" in button.text:
                if len(self.words_label.text) and self.words_label.text[-1] == button.text[0]:
                    self.words_label.text = self.words_label.text[:-1] + button.text[-1]
                else:
                    self.words_label.text += button.text[0]
            else:
                self.words_label.text += button.text

    def check_guess(self, instance) -> None:
        guess = self.words_label.text
        self.words_label.text = ''

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
            return

        if self.current_attempt >= self.max_attempts:
            self.result_label.text += f"\n\n[size=20]You lost! The word was: [b]{self.secret_word}[/b][/size]"
            return

    def color_letter(self, letter: str, color: str) -> None:
        for row_grid in self.keyboard_layout.children:
            for btn in row_grid.children:
                if letter in btn.text:
                    btn.background_color = color
                    return

    def evaluate_guess(self, guess: str) -> str:
        result = ""
        for i, letter in enumerate(guess):
            if letter == self.secret_word[i]:
                color = GREEN_COLOR
                result += f"[color=#{color}]{letter}[/color]"  # Correct letter in correct position
            elif letter in self.secret_word:
                color = YELLOW_COLOR
                result += f"[color=#{color}]{letter}[/color]"  # Correct letter in wrong position
            else:
                color = BLACK_COLOR
                result += f"[color=#fc0303]{letter}[/color]"  # Incorrect letter

            self.color_letter(letter, color)

        return f"[b]{result}[/b]"

    def show_popup(self, title: str, message: str) -> None:
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class WordleApp(App):

    def build(self):
        return WordleLayout()


if __name__ == "__main__":
    WordleApp().run()
