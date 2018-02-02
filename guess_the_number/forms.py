from django import forms


class InitializeForm(forms.Form):
    player_type = forms.ChoiceField(label='Выберите тип игры: ', widget=forms.RadioSelect,
                                    choices=(('one', 'Один игрок'), ('two', 'Два игрока')), initial='one')

    game_type = forms.ChoiceField(widget=forms.RadioSelect,
                                  choices=(('1', 'Угадать число'), ('2', 'Загадать число')), initial='1')
    how_many_digits = forms.IntegerField(label='Сколько цифр в загаданном числе?', max_value=10, min_value=1, initial=5)

class GameWithComputerForm(forms.Form):
    cows = forms.IntegerField(label='Коровы', max_value=10, min_value=1)
    bulls = forms.IntegerField(label='Быки', max_value=10, min_value=1)