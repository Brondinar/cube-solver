from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.core.cache import cache


from .forms import InitializeForm
from .models import GameData

from random import choice
from itertools import permutations, combinations


def home_page(request):
    return render(request, 'guessthenumber/home.html')

def game_index(request):
    if request.method == 'POST':
        form = InitializeForm(request.POST)
        if form.is_valid():
            how_many_digits = int(request.POST['how_many_digits'])
            # game_id должен быть уникальным для каждой игры
            game_id = request.session['_auth_user_id']
            request.session['game_type'] = request.POST['game_type']
            if request.POST['game_type'] == '1':
                secret_number = ''.join(choice(list(permutations("0123456789", how_many_digits))))
                # game_data = GameData(id=game_id, secret_number=secret_number, move=1, cows=0, bulls=0)
                # game_data.save()
                cache.set(game_id, {'secret_number': secret_number, 'move': 1, 'cows': 0, 'bulls': 0,
                                    'digits': how_many_digits})
                return redirect('/guessthenumber/game/')
            else:
                all_numbers = list(permutations("0123456789", how_many_digits))
                cache.set(game_id, {'all_numbers': all_numbers, 'move': 1, 'digits': how_many_digits,
                                    'my_number': ''.join(choice(all_numbers)), 'game_over': False})
                return redirect('/guessthenumber/game/')
    else:
        form = InitializeForm()

    return render(request, 'guessthenumber/index.html', {'form': form})


# обрабатывает данные, полученные от игрока и отправляет ответ. Работает только для "игры человека"
def game_process(request):
    # game = GameData.objects.get(pk=game_id)
    game = cache.get(request.session['_auth_user_id'])
    def game_with_human():
        class GameWithHumanForm(forms.Form):
            player_number = forms.CharField(label='Ваше число', max_length=game['digits'],
                                            validators=[RegexValidator(regex=r'^\d*$', message='Введите корректное число.'),
                                                        MinLengthValidator(game['digits'],
                                                                           message='Число должно состоять из %s символов.'
                                                                                   % game['digits'])])

        if request.method == 'POST':
            form = GameWithHumanForm(request.POST)
            # game.update({'form': form})
            if form.is_valid():
                player_number = request.POST.get('player_number')
                game['move'] += 1
                game['cows'] = len([1 for c in player_number if (c in game['secret_number'])])
                game['bulls'] = len([1 for c in range(game['digits']) if game['secret_number'][c] == player_number[c]])
                # проверка предназначена для корректного отображения ходов. Выглядит стремно, стоит переделать.
                if game['bulls'] == game['digits']:
                    game['move'] -= 1
                # следующие две строки служат для удаления введенных значений после обновления формы, поскольку
                # request.POST их автоматически вносит, а без него form.is_valid() выдает false. Возможно, стоит
                # переделать.
                form = GameWithHumanForm()
                # game.update({'form': form})

        else:
            form = GameWithHumanForm()
            # game.update({'form': form})

        cache.set(request.session['_auth_user_id'], game)
        game.update({'form': form})
        return render(request, 'guessthenumber/player_game.html', game)

    def game_with_computer():

        class GameWithComputerForm(forms.Form):
            is_correct_number = forms.ChoiceField(label='Я угадал?', widget=forms.RadioSelect,
                                                  choices=(('1', 'Да'), ('2', 'Нет')), initial=2)
            cows = forms.IntegerField(label='Коровы:', max_value=game['digits'], min_value=0, initial=0)
            bulls = forms.IntegerField(label='Быки:', max_value=game['digits'], min_value=0, initial=0)

        if request.method == 'POST':
            form = GameWithComputerForm(request.POST)
            if form.is_valid():
                if request.POST['is_correct_number'] == '1':
                    game['game_over'] = True
                    return render(request, 'guessthenumber/computer_game.html', game)

                # фильтрует варианты по "коровам"
                def cows_filter(cows, number, variants):
                    possible_variants = []
                    pos_comb = list(combinations(number, cows))
                    for comb in pos_comb:
                        for num in variants:
                            if set(num).issubset(set(num)) and set(
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
                game['all_numbers'] = cows_filter(game['cows'], game['my_number'], game['all_numbers'])

                try:
                    game['my_number'] = ''.join(choice(game['all_numbers']))
                except IndexError:
                    game['error_message'] = 'Одно из полученных условий противоречит другому: такого числа не ' \
                                            'существует.'
                    return HttpResponse(game['error_message'] +
                                        '<br><a id="id_return" href="/guessthenumber/">Вернуться назад</a>')

                form = GameWithComputerForm()
        else:
            form = GameWithComputerForm()

        cache.set(request.session['_auth_user_id'], game)
        game.update({'form': form})
        return render(request, 'guessthenumber/computer_game.html', game)

    if request.session['game_type'] == '1':
        return game_with_human()
    else:
        return game_with_computer()