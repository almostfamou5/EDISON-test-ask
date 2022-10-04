from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from num_app.forms import NumberForm
from django.urls import reverse
from .utils import Game


def session_check(request):
    if 'game' not in request.session:
        game = Game()
        request.session['game'] = game
        return HttpResponseRedirect(reverse('start'))
    else:
        return request


class StartGameView(View):

    @staticmethod
    def get(request):
        template_name = 'num_app/start_template.html'
        session_check(request)
        game = request.session['game']
        user_history = game.player.numbers_list
        psychs = game.psychics_factory.get_psychics_list()
        context = {'psychics': psychs, 'user_history': user_history}
        return render(request, template_name, context)

    @staticmethod
    def post(request):
        session_check(request)
        game = request.session['game']
        game.psychics_factory.make_guess()
        return HttpResponseRedirect(reverse('write_your_number'))


class InputYourNumberView(View):

    @staticmethod
    def get(request):
        template_name = 'num_app/number_input_template.html'
        session_check(request)
        number_form = NumberForm()
        game = request.session['game']
        user_history = game.player.numbers_list
        psychs = game.psychics_factory.get_psychics_list()
        context = {'psychics': psychs, 'number_form': number_form, 'user_history': user_history}
        return render(request, template_name, context)

    @staticmethod
    def post(request):
        session_check(request)
        number_form = NumberForm(request.POST)
        game = request.session['game']
        if number_form.is_valid():
            game.psychics_factory.check_guess_all(number_form.cleaned_data.get('number'))
            game.player.save_number(number_form.cleaned_data.get('number'))
            return HttpResponseRedirect(reverse('start'))
        else:
            return HttpResponseRedirect(reverse('write_your_number'))


