from pynames.generators.russian import PaganNamesGenerator
import random


class Game:
    def __init__(self):
        self.player = Player()
        self.psychics_factory = PsychicsFactory()


class Psychics:

    def __init__(self):
        self.name = PaganNamesGenerator().get_name_simple()
        self.psych_guess = 0
        self.accuracy_level = 0
        self.answer_list = []

    def guess(self):
        # attempt to guess the number
        self.psych_guess = random.randint(10, 99)
        self.answer_list.append(self.psych_guess)

    def get_accuracy(self):
        return self.accuracy_level

    def guess_check(self, user_answer):
        # checking the psychic's guess
        if user_answer == self.psych_guess:
            self.accuracy_level += 1
        else:
            self.accuracy_level -= 1


class PsychicsFactory:
    def __init__(self):
        self.psychics = [Psychics() for _ in range(2, 4)]

    def get_psychics_list(self):
        return [psych for psych in self.psychics]

    def make_guess(self):
        [psych.guess() for psych in self.psychics]

    def check_guess_all(self, user_answer):
        [psych.guess_check(user_answer) for psych in self.psychics]


class Player:
    def __init__(self):
        self.numbers_list = []

    def save_number(self, number):
            self.numbers_list.append(number)