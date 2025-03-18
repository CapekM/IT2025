import itertools
import random

from collections import defaultdict
from kivy.app import App
from kivy.core.audio.audio_sdl2 import SoundLoader, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager, SwapTransition

from utils import GREEN_COLOR, YELLOW_COLOR, BLACK_COLOR, GamePages, get_similar_letter, get_word_list


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def switch_to_page(self, page_name: GamePages) -> None:
        self.current = page_name
        if page_name in [GamePages.GAME, GamePages.WELCOME]:
            # Each screen has only one children, which is our Page class
            self.current_screen.children[0].setup()

    def add_page(self, widget, page_name: GamePages, **kwargs):
        screen = Screen(name=page_name)
        screen.add_widget(widget)
        super().add_widget(screen, **kwargs)


class WelcomePage(BoxLayout):
    def __init__(self, screen_manager: MyScreenManager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager

        self.play_button = self.ids.play_button
        self.settings_button = self.ids.settings_button
        self.setup()

    def setup(self):
        Clock.schedule_once(self._check_size_once)

    def _check_size_once(self, dt):
        if self.size == [100, 100]:  # If still default size, wait another frame
            Clock.schedule_once(self._check_size_once)
        else:
            y_to_go = self.play_button.y
            self.play_button.y = 0
            animation = Animation(background_color=[0, 0, 1, 1], duration=1.3, y=y_to_go)
            animation.start(self.play_button)

            animation = Animation(background_color=[0, 1, 0, 1], duration=2)
            animation.start(self.settings_button)

    def switch_to_game_page(self, instance):
        wordle_app.screen_manager.switch_to_page(GamePages.GAME)

    def switch_to_settings_page(self, instance):
        wordle_app.screen_manager.switch_to_page(GamePages.SETTINGS)


class OverPage(BoxLayout):
    def __init__(self, screen_manager: MyScreenManager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.name_label = self.ids.name_label

        self.sound_win = SoundLoader.load("assets/win_sound.wav")
        self.sound_lose = SoundLoader.load("assets/loss_sound.wav")
        self.sound_on = True

    def switch_sound(self) -> bool:
        self.sound_on = not self.sound_on
        self.sound_win.volume = int(self.sound_on)
        self.sound_lose.volume = int(self.sound_on)
        return self.sound_on

    def switch_to_over_page(self, won: bool, word: str, attempts: int):
        if won:
            self.name_label.text = f"Congratulations!\nYou guessed {word}.\nIt took you {attempts} attempts."
            self.sound_win.play()
        else:
            self.name_label.text = f"You lost!\nThe word was {word}."
            self.sound_lose.play()

        wordle_app.screen_manager.switch_to_page(GamePages.OVER)

    def switch_to_welcome_page(self, instance):
        wordle_app.screen_manager.switch_to_page(GamePages.WELCOME)

    def switch_to_game_page(self, instance):
        wordle_app.screen_manager.switch_to_page(GamePages.GAME)


class SettingsPage(BoxLayout):
    def __init__(self, screen_manager: MyScreenManager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager

    def switch_sound(self):
        sound_on = wordle_app.over_page.switch_sound()
        if sound_on:
            self.ids.play_button.text = "Sound ON"
        else:
            self.ids.play_button.text = "Sound OFF"

    def switch_to_welcome_page(self):
        wordle_app.screen_manager.switch_to_page(GamePages.WELCOME)


class KeyboardButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

    def setup(self) -> None:
        self.background_color = "FFFFFF"

    def change_color(self, color: str) -> None:
        if self.background_color == GREEN_COLOR:
            return
        if self.background_color == YELLOW_COLOR and color == BLACK_COLOR:
            return

        self.background_color = color


class GamePage(BoxLayout):
    def __init__(self, screen_manager: MyScreenManager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.word_list: list[str] = get_word_list()
        self.secret_word = random.choice(self.word_list)
        self.words_len = 5
        self.max_attempts = 5
        self.current_attempt = 0

        self.result_label = self.ids.result_label
        self.words_label = self.ids.words_label
        self.submit_button = self.ids.submit_button
        self.keyboard_layout = self.ids.keyboard_layout

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

        # Structures for hints
        self.matching_letters: dict[str, list[int]] = {}
        self.known_letters: dict[str, list[int]] = {}
        self.banned_letters: list[str] = []

    def setup(self):
        self.secret_word = random.choice(self.word_list)
        self.result_label.text = ""
        self.words_label.text = "LÁSKA"  # TODO delete, it is for debugging purposes
        self.current_attempt = 0
        for row_grid in self.keyboard_layout.children:
            btn: KeyboardButton
            for btn in row_grid.children:
                btn.setup()
        self.matching_letters = defaultdict(list)
        self.known_letters = defaultdict(list)
        self.banned_letters = []

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

    def _word_match(self, word: str) -> bool:
        for letter, positions in self.matching_letters.items():
            for position in positions:
                if "/" in letter:
                    if letter[0] != word[position] and letter[-1] != word[position]:
                        return False
                elif letter != word[position]:
                    return False

        for letter, positions in self.known_letters.items():
            # Check letter is not on position it cannot be
            for position in positions:
                if "/" in letter:
                    if letter[0] == word[position] or letter[-1] == word[position]:
                        return False
                elif letter == word[position]:
                    return False

            # Check letter is in word
            if "/" in letter:
                if letter[0] not in word[position] or letter[-1] not in word[position]:
                    return False
            elif letter not in word:
                return False



        for letter in self.banned_letters:
            if "/" in letter:
                if letter[0] in word or letter[-1] in word:
                    return False
            elif letter in word:
                return False

        return True

    def _find_matching_candidate(self) -> list[str]:
        """
        Find mathing words. Shuffle and return 5 of them.
        """
        result = []
        for word in self.word_list:
            if self._word_match(word):
                result.append(word)
        random.shuffle(result)
        return result[:5]

    def show_hint(self) -> None:
        candidates = self._find_matching_candidate()
        self.show_popup("Hint", "\n".join(candidates))

    def check_guess(self) -> None:
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
            wordle_app.over_page.switch_to_over_page(True, self.secret_word, self.current_attempt)

        elif self.current_attempt >= self.max_attempts:
            self.result_label.text += f"\n\n[size=20]You lost! The word was: [b]{self.secret_word}[/b][/size]"
            wordle_app.over_page.switch_to_over_page(False, self.secret_word, self.current_attempt)

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
                self.matching_letters[letter].append(i)
            elif letter in self.secret_word or (similar_letter is not None and similar_letter in self.secret_word[i]):
                color = YELLOW_COLOR
                result += f"[color=#{color}]{letter}[/color]"  # Correct letter in wrong position
                self.known_letters[letter].append(i)
            else:
                color = BLACK_COLOR
                result += f"[color=#fc0303]{letter}[/color]"  # Incorrect letter
                self.banned_letters.append(letter)

            self.color_letter(letter, color)

        return f"[b]{result}[/b]"

    def show_popup(self, title: str, message: str) -> None:
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class WordleApp(App):

    def build(self):
        self.title = "Wordle"
        self.screen_manager = MyScreenManager(transition=SwapTransition())

        self.welcome_page = WelcomePage(self.screen_manager)
        self.screen_manager.add_page(self.welcome_page, GamePages.WELCOME)

        self.game_page = GamePage(self.screen_manager)
        self.screen_manager.add_page(self.game_page, GamePages.GAME)

        self.over_page = OverPage(self.screen_manager)
        self.screen_manager.add_page(self.over_page, GamePages.OVER)

        self.settings_page = SettingsPage(self.screen_manager)
        self.screen_manager.add_page(self.settings_page, GamePages.SETTINGS)

        return self.screen_manager


if __name__ == "__main__":
    wordle_app = WordleApp()
    wordle_app.run()
