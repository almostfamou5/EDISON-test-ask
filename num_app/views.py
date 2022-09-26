from django.http import HttpResponseRedirect
from django.shortcuts import render
from num_app.forms import NumberForm
from django.urls import reverse
import random


class Psychics:

    def __init__(self, psych_guess=0, accuracy_level = 0, try_count=0):
        name_list = ['Паша', 'Даша', 'Глаша', 'Маша', 'Саша', 'Наташа', 'Аркаша']
        self.psych_guess = psych_guess
        self.try_count = try_count
        self.accuracy_level = accuracy_level
        self.name = random.choice(name_list)
        self.answer_list = []

    def guess(self):
        # attempt to guess the number
        self.psych_guess = random.randint(10, 99)
        self.answer_list.append(self.psych_guess)

    def guess_check(self, user_answer):
        # checking the psychic's guess
        if user_answer == self.psych_guess:
            self.accuracy_level += 1
        else:
            self.accuracy_level -= 1
        self.try_count += 1


def session_check(request):
    if 'psychics' not in request.session:
        psychs = [Psychics() for _ in range(random.randint(2, 4))]
        request.session['psychics'] = psychs
        request.session['user_history'] = []
        return HttpResponseRedirect(reverse('start'))
    else:
        return request


def start_game(request):
    if request.method == 'GET':
        session_check(request)
        user_history = request.session['user_history']
        psychs = [psych for psych in request.session['psychics']]
        return render(request, 'num_app/start_template.html', {'psychics': psychs, 'user_history': user_history})

    if request.method == 'POST':
        session_check(request)
        psychs = [psych for psych in request.session['psychics']]
        [psych.guess() for psych in psychs]
        return HttpResponseRedirect(reverse('write_your_number'))


def input_your_number(request):
    if request.method == 'GET':
        session_check(request)
        number_form = NumberForm()
        user_history = request.session['user_history']
        psychs = [psych for psych in request.session['psychics']]
        return render(request, 'num_app/number_input_template.html',
                      {'psychics': psychs, 'number_form': number_form, 'user_history': user_history})

    if request.method == 'POST':
        session_check(request)
        number_form = NumberForm(request.POST)
        psychs = [psych for psych in request.session['psychics']]
        if number_form.is_valid():
            [psych.guess_check(number_form.cleaned_data.get('number')) for psych in psychs]
            request.session['user_history'].append(number_form.cleaned_data.get('number'))
            return HttpResponseRedirect(reverse('start'))
        else:
            return HttpResponseRedirect(reverse('write_your_number'))

