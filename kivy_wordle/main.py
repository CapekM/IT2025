import itertools
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
    return [x.upper() for x in words_file_path.read_text(encoding="utf-8").strip().splitlines()]


class KeyboardButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = "FFFFFF"

    def change_color(self, color: str) -> None:
        if self.background_color == GREEN_COLOR:
            return
        if self.background_color == YELLOW_COLOR and color == BLACK_COLOR:
            return

        self.background_color = color


def get_similar_letter(couple_letters: list[tuple[str, str]], letter: str) -> str | None:
    for couple in couple_letters:
        if letter == couple[0]:
            return couple[1]
        elif letter == couple[1]:
            return couple[0]
    return None


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

        self.words_label.text = "LASKA"  # TODO delete, it is for debugging purposes

        self.couple_letters: list[tuple[str, str]] = []
        keyboard_layout = [
            ["Ú/Ů", "Č", "Ě", "Ř", "Š", "Ž"],
            ["W", "E/É", "R", "T/Ť", "Y/Ý", "U", "I/Í", "O/Ó", "P"],
            ["A/Á", "S", "D/Ď", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "M", "N/Ň", "<-"],
        ]
        for row in keyboard_layout:
            keyboard_row_layout = BoxLayout()
            for key in row:
                if "/" in key:
                    assert len(key) == 3, f"Key with / does not have len 3. {key =}"
                    self.couple_letters.append((key[0], key[-1]))
                button = KeyboardButton(text=key, on_press=self.on_key_press)
                keyboard_row_layout.add_widget(button)
            self.keyboard_layout.add_widget(keyboard_row_layout)

    def on_key_press(self, button):
        if button.text == "<-":
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
        elif (
            len(self.words_label.text) == self.words_len
            and "/" in button.text
            and self.words_label.text[-1] == button.text[0]
        ):
            self.words_label.text = self.words_label.text[:-1] + button.text[-1]

    def check_guess(self, instance) -> None:
        guess = self.words_label.text

        if len(guess) != 5:
            self.show_popup("Invalid Guess", "Please enter a 5-letter word.")
            return

        if not self.check_guess_in_words(guess):
            self.show_popup("Invalid Word", "This word is not in the list.")
            return

        self.words_label.text = ""
        self.current_attempt += 1
        result = self.evaluate_guess(guess)

        # Display result of the guess
        if not self.result_label.text:
            self.result_label.text += f"Attempt {self.current_attempt}: {result}"
        else:
            self.result_label.text += f"\nAttempt {self.current_attempt}: {result}"

        if guess == self.secret_word:
            self.result_label.text += (
                f"\n\n[size=20]Congratulations! You guessed the word: [b]{self.secret_word}[/b][/size]"
            )
            return

        if self.current_attempt >= self.max_attempts:
            self.result_label.text += f"\n\n[size=20]You lost! The word was: [b]{self.secret_word}[/b][/size]"
            return

    def check_guess_in_words(self, guess: str) -> bool:
        couple_letters_flat = [l for couple in self.couple_letters for l in couple]
        couple_indices = [i for i, letter in enumerate(guess) if letter in couple_letters_flat]

        for combination_len in range(len(couple_indices) + 1):
            for indices_to_change in itertools.combinations(couple_indices, combination_len):
                changed_guess = ""
                for i, l in enumerate(guess):
                    if i in indices_to_change:
                        changed_guess += get_similar_letter(self.couple_letters, l)
                    else:
                        changed_guess += l
                print(f"{combination_len = }, {changed_guess = }, {indices_to_change = }")
                if changed_guess in self.word_list:
                    return True

        return False

    def color_letter(self, letter: str, color: str) -> None:
        for row_grid in self.keyboard_layout.children:
            btn: KeyboardButton
            for btn in row_grid.children:
                if letter in btn.text:
                    btn.change_color(color)
                    return

    def evaluate_guess(self, guess: str) -> str:
        result = ""
        for i, letter in enumerate(guess):
            similar_letter = get_similar_letter(self.couple_letters, letter)
            if letter == self.secret_word[i] or (similar_letter is not None and similar_letter == self.secret_word[i]):
                color = GREEN_COLOR
                result += f"[color=#{color}]{letter}[/color]"  # Correct letter in correct position
            elif letter in self.secret_word or (similar_letter is not None and similar_letter in self.secret_word[i]):
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
