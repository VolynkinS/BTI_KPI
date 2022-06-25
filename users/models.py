from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from kpi.models import UserAnswer


# https://django.fun/tutorials/django-custom-user-model/


class CustomUser(AbstractUser):
    patronymic = models.CharField(max_length=75, blank=True, verbose_name='Отчество')
    total_points = models.FloatField(default=0, verbose_name='Общее количество баллов')

    class Meta:
        verbose_name = 'Преподователь'
        verbose_name_plural = 'Преподователи'
        ordering = ['pk']

    def get_amount_points(self):
        return UserAnswer.objects.filter(user_id=self.pk).aggregate(amounts=Sum('point'))['amounts']

    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'


    def __str__(self):
        return self.full_name() if self.full_name().strip() != '' else self.username
