from django import forms


class InitializeForm(forms.Form):
    game_type = forms.ChoiceField(label='Выберите тип игры: ', widget=forms.RadioSelect,
                                  choices=(('1', 'Угадать число'), ('2', 'Загадать число')))
    how_many_digits = forms.IntegerField(label='Сколько цифр в загаданном числе?', max_value=10, min_value=1, initial=5)

class GameWithComputerForm(forms.Form):
    cows = forms.IntegerField(label='Коровы', max_value=10, min_value=1)
    bulls = forms.IntegerField(label='Быки', max_value=10, min_value=1)