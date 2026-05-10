from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Locations(models.Model):
    """
    name - Название
    user_id - Пользователь, добавивший эту локацию
    latitude - Широта локации
    longitude - Долгота локации
    """
    name = models.CharField()
    user_id = models.ManyToManyField(User)
    latitude = models.DecimalField(max_digits=12, decimal_places=9)
    longitude = models.DecimalField(max_digits=12, decimal_places=9)

    def __str__(self):
        return self.name