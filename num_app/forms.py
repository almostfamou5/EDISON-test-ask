from django import forms


class NumberForm(forms.Form):
    number = forms.IntegerField(label='Введите загаданное число', min_value=10, max_value=99)
