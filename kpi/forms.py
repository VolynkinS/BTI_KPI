from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm

from kpi.models import Indicator, UserAnswer


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class UserAnswerForm(ModelForm):
    indicator = forms.ModelChoiceField(queryset=Indicator.objects.all(), disabled=True,
                                       widget=forms.Select(attrs={'class': 'form-control'}), label='Показатель')
    point = forms.FloatField(min_value=-10, disabled=True, required=False,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Балл')
    text = forms.CharField(disabled=True, required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = UserAnswer
        fields = ['indicator', 'point', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
        help_text = {'point': 'Введите балл', 'text': 'Введите ФИО ваших подопечных, если требуется'}


class NumberStudentsForm(forms.Form):
    students_all = forms.IntegerField(label='Всего воспитанников',
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    students_ok = forms.IntegerField(label='Кол-во подходящих к показателю воспитанников',
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))


class AmountEventForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
