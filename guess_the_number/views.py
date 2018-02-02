from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.db import models


from .forms import InitializeForm
from .models import OnlineGameData

from random import choice
from itertools import permutations, combinations


def home_page(request):
    return render(request, 'guess_the_number/home.html')

def game_index(request):
    if request.method == 'POST':
        form = InitializeForm(request.POST)
        if form.is_valid():

            # блок кода для одного игрока
            if request.POST['player_type'] == 'one':
                how_many_digits = int(request.POST['how_many_digits'])
                game_id = request.session.session_key
                request.session['game_type'] = request.POST['game_type']
                if request.POST['game_type'] == '1':
                    secret_number = ''.join(choice(list(permutations("0123456789", how_many_digits))))
                    # game_data = GameData(id=game_id, secret_number=secret_number, move=1, cows=0, bulls=0)
                    # game_data.save()
                    cache.set(game_id, {'secret_number': secret_number, 'move': 1, 'cows': 0, 'bulls': 0,
                                        'digits': how_many_digits, 'player_numbers': []})
                else:
                    all_numbers = list(permutations("0123456789", how_many_digits))
                    cache.set(game_id, {'all_numbers': all_numbers, 'move': 1, 'digits': how_many_digits,
                                        'my_number': ''.join(choice(all_numbers)), 'game_over': False})
                return redirect('/guess_the_number/game/')

            # блок кода для двух игроков
            else:
                player = request.session.session_key
                waiting_players = cache.get('waiting_players')
                if waiting_players is None:
                    cache.set('waiting_players', {'players': player})
                elif player not in waiting_players['players']:
                    waiting_players['players'].append(player)
                    cache.set('waiting_players', waiting_players['players'])
                redirect('/guess_the_number/online-game/')
    else:
        form = InitializeForm()

    return render(request, 'guess_the_number/index.html', {'form': form})


# обрабатывает данные, полученные от игрока и отправляет ответ. Работает только для "игры человека"
def game_process(request):
    # game = GameData.objects.get(pk=game_id)
    game = cache.get(request.session.session_key)
    if game is None:
        return HttpResponseForbidden("""<p>Время сессии вышло. Вернитесь назад, чтобы начать сначала.</p>
                            <a class="return" href="/guess_the_number/">Вернуться назад</a>""")

    def game_with_human():
        class GameWithHumanForm(forms.Form):
            player_number = forms.CharField(label='Ваше число', max_length=game['digits'],
                                            validators=[RegexValidator(regex=r'^\d*$', message='Ввод должен содержать только цифры'),
                                                        MinLengthValidator(game['digits'],
                                                                           message='Число должно состоять из %s символов.'
                                                                                   % game['digits'])])

        if request.method == 'POST':
            form = GameWithHumanForm(request.POST)
            # game.update({'form': form})
            if form.is_valid():
                player_number = request.POST.get('player_number')
                game['bulls'] = len([1 for c in range(game['digits']) if game['secret_number'][c] == player_number[c]])
                game['cows'] = len([1 for c in player_number if (c in game['secret_number'])]) - game['bulls']

                # логирует данные каждый ход игры для последующего отображения
                game['player_numbers'].append({'move': game['move'], 'number': player_number, 'cows': game['cows'],
                                               'bulls': game['bulls']})

                if game['bulls'] != game['digits']:
                    game['move'] += 1
                # следующие две строки служат для удаления введенных значений после обновления формы, поскольку
                # request.POST их автоматически вносит, а без него form.is_valid() выдает false. Возможно, стоит
                # переделать.
                form = GameWithHumanForm()

        else:
            form = GameWithHumanForm()

        cache.set(request.session.session_key, game)
        game.update({'form': form})
        return render(request, 'guess_the_number/player_game.html', game)

    def game_with_computer():

        class GameWithComputerForm(forms.Form):
            # is_correct_number = forms.ChoiceField(label='Я угадал?', widget=forms.RadioSelect,
            #                                       choices=(('1', 'Да'), ('2', 'Нет')), initial=2)
            cows = forms.IntegerField(label='Коровы:', max_value=game['digits'], min_value=0, initial=0)
            bulls = forms.IntegerField(label='Быки:', max_value=game['digits'], min_value=0, initial=0)

        if request.method == 'POST':
            form = GameWithComputerForm(request.POST)
            if form.is_valid():
                if request.POST['is_correct_number'] == '1':
                    game['game_over'] = True
                    return render(request, 'guess_the_number/computer_game.html', game)

                # фильтрует варианты по "коровам"
                def cows_filter(cows_and_bulls, number, variants):
                    possible_variants = []
                    pos_comb = list(combinations(number, cows_and_bulls))
                    for comb in pos_comb:
                        for num in variants:
                            if set(comb).issubset(set(num)) and set(
                                            set(number) ^ set(comb)).isdisjoint(num):
                                possible_variants.append(num)
                    return possible_variants

                # фильтрует варианты по "быкам"
                def bulls_filter(bulls, number, variants):
                    possible_variants = []
                    n = 0
                    for num in variants:
                        for i in range(len(number)):
                            if num[i] == number[i]:
                                n += 1
                        if n == bulls:
                            possible_variants.append(num)
                        n = 0
                    return possible_variants

                game['cows'] = int(request.POST.get('cows'))
                game['bulls'] = int(request.POST.get('bulls'))
                game['move'] += 1

                game['all_numbers'] = bulls_filter(game['bulls'], game['my_number'], game['all_numbers'])
                game['all_numbers'] = cows_filter(game['cows'] + game['bulls'], game['my_number'], game['all_numbers'])

                try:
                    game['my_number'] = ''.join(choice(game['all_numbers']))
                except IndexError:
                    game['error_message'] = 'Одно из полученных условий противоречит другому: такого числа не ' \
                                            'существует.'
                    return HttpResponse(game['error_message'] +
                                        '<br><a id="id_return" href="/guess_the_number/">Вернуться назад</a>')

                form = GameWithComputerForm()
        else:
            form = GameWithComputerForm()

        cache.set(request.session.session_key, game)
        game.update({'form': form})
        return render(request, 'guess_the_number/computer_game.html', game)

    if request.session['game_type'] == '1':
        return game_with_human()
    else:
        return game_with_computer()

def multiplayer_process(request):
    pass