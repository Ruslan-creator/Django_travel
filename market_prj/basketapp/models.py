import datetime

from django.conf import settings
from django.db import models

from mainapp.models import Accommodation


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="basket"
    )
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    nights = models.PositiveIntegerField(verbose_name="кол-во ночей", default=0, blank=True, null=True)
    add_datetime = models.DateTimeField(verbose_name="время", auto_now_add=True)
    date_from = models.DateTimeField(verbose_name="Прибытие", blank=True, null=True, default=datetime.datetime.now())
    date_to = models.DateTimeField(verbose_name="Выезд", blank=True, null=True, default=datetime.datetime.now())

    # стоимость одного предложения компании
    @property
    def accommodation_cost(self):
        return self.accommodation.price * self.nights

    # общее количество ночей по всем заказам в корзине
    @property
    def total_nights(self):
        _accommodation = Basket.objects.filter(user=self.user)
        _total_nights = sum(list(map(lambda x: x.nights, _accommodation)))
        return _total_nights

    # общая стоимость всех предложений пользователя в корзине
    @property
    def total_cost(self):
        _accommodation = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.accommodation_cost, _accommodation)))
        return _total_cost

    # количество заказов пользователя в корзине
    @staticmethod
    def get_items(user):
        return user.basket.select_related().order_by("accommodation__country")
