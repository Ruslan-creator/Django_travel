"""Формы используемые для страниц на сайте."""
from django import forms
from django.utils import timezone
from basketapp.models import Basket
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from market_prj import settings

df = settings.DATE_INPUT_FORMATS


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = "__all__"

    date_from = forms.DateTimeField(
        label="Прибытие",
        input_formats=df,
        initial=lambda: timezone.now().astimezone().strftime(df[0]),
        widget=DateTimePickerInput(
            format=df[0],
            options={
                "locale": "ru",
                "showClose": True,
                "showClear": False,
                "showTodayButton": True,
            },
        ),
    )
    date_to = forms.DateTimeField(
        label="Выезд",
        input_formats=df,
        initial=lambda: timezone.now().astimezone().strftime(df[0]),
        widget=DateTimePickerInput(
            format=df[0],
            options={
                "locale": "ru",
                "showClose": True,
                "showClear": False,
                "showTodayButton": True,
            },
        ),
    )
