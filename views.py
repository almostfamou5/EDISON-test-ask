from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from num_app.forms import NumberForm
from django.urls import reverse
from .utils import PsychicsFactory, Player


def session_check(request):
    if 'psychics' not in request.session:
        psychs = PsychicsFactory().psychics
        request.session['psychics'] = psychs
        player = Player()
        request.session['user_history'] = player.numbers_list
        return HttpResponseRedirect(reverse('start'))
    else:
        return request


class StartGameView(View):

    @staticmethod
    def get(request):
        template_name = 'num_app/start_template.html'
        session_check(request)
        user_history = request.session['user_history']
        psychs = [psych for psych in request.session['psychics']]
        context = {'psychics': psychs, 'user_history': user_history}
        return render(request, template_name, context)

    @staticmethod
    def post(request):
        session_check(request)
        psychs = [psych for psych in request.session['psychics']]
        [psych.guess() for psych in psychs]
        return HttpResponseRedirect(reverse('write_your_number'))


class InputYourNumberView(View):

    @staticmethod
    def get(request):
        template_name = 'num_app/number_input_template.html'
        session_check(request)
        number_form = NumberForm()
        user_history = request.session['user_history']
        psychs = [psych for psych in request.session['psychics']]
        context = {'psychics': psychs, 'number_form': number_form, 'user_history': user_history}
        return render(request, template_name, context)

    @staticmethod
    def post(request):
        session_check(request)
        number_form = NumberForm(request.POST)
        psychs = [psych for psych in request.session['psychics']]
        if number_form.is_valid():
            [psych.guess_check(number_form.cleaned_data.get('number')) for psych in psychs]
            request.session['user_history'].append(number_form.cleaned_data.get('number'))
            return HttpResponseRedirect(reverse('start'))
        else:
            return HttpResponseRedirect(reverse('write_your_number'))


