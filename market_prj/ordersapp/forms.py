from django import forms
from django.utils import timezone
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from market_prj import settings

df = settings.DATE_INPUT_FORMATS

from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["date_from", "date_to"]

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

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
