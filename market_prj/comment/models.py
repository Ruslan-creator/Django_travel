from django.db import models
from mainapp.models import Accommodation
from authapp.models import TravelUser, TravelUserProfile


class Comment(models.Model):
    date = models.DateTimeField(verbose_name="дата", auto_now_add=True)
    text = models.TextField(verbose_name="текст", blank=True)
    accommodation_id = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    travel_user_profile_id = models.ForeignKey(TravelUserProfile, on_delete=models.CASCADE)
    travel_user_id = models.ForeignKey(TravelUser, on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)

    def __str__(self):
        return self.text
