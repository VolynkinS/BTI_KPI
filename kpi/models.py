from django.db import models
from django.urls import reverse_lazy


class Kpi(models.Model):
    name = models.CharField(max_length=250, db_index=True, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Показатель эффективности деятельности'
        verbose_name_plural = '1. Показатели эффективности деятельности'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse_lazy('kpi:home', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.pk}: {self.name}'


class Criteria(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    kpi = models.ForeignKey('Kpi', on_delete=models.PROTECT, verbose_name='Показатель эффективности деятельности')

    class Meta:
        verbose_name = 'Критерий оценки эффективности деятельности'
        verbose_name_plural = '2. Критерии оценки эффективности деятельности'
        ordering = ['id']

    def __str__(self):
        return f'{self.kpi.pk}: {self.name}'


class Indicator(models.Model):
    name = models.CharField(max_length=250, db_index=True, verbose_name='Наименование')
    criteria = models.ForeignKey('Criteria', on_delete=models.PROTECT,
                                 verbose_name='Критерий оценки эффективности деятельности')
    category = models.ManyToManyField('Category', verbose_name='Категории')

    class Meta:
        verbose_name = 'Количественный, качественный или объёмный показатель'
        verbose_name_plural = '3. Количественные, качественные или объёмные показатели'
        ordering = ['id']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    condition = models.ForeignKey('Condition', on_delete=models.PROTECT, blank=True, null=True)
    condition3 = models.ForeignKey('Condition3', on_delete=models.PROTECT, blank=True, null=True)
    point = models.FloatField(verbose_name='Балл')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = '4. Категории'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}: {self.point}'


class Condition(models.Model):
    percent_min = models.IntegerField(verbose_name='Минимальный процент')
    percent_max = models.IntegerField(verbose_name='Максимальный процент')

    class Meta:
        verbose_name = 'Условие 1'
        verbose_name_plural = '5.1 Условия'
        ordering = ['id']

    def __str__(self):
        return f'{self.percent_min}-{self.percent_max}%'


class Condition3(models.Model):
    amount_min = models.IntegerField(verbose_name='Минимальное количество')
    amount_max = models.IntegerField(verbose_name='Максимальное количество')

    class Meta:
        verbose_name = 'Условие 3'
        verbose_name_plural = '5.3 Условия'
        ordering = ['id']

    def __str__(self):
        return f'{self.amount_min}-{self.amount_max}'


class UserAnswer(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, verbose_name='Преподаватель')
    indicator = models.ForeignKey('Indicator', on_delete=models.PROTECT, verbose_name='Показатель')
    point = models.FloatField(blank=True, null=True, verbose_name='Балл')
    text = models.TextField(max_length=1700, blank=True)
    approve = models.BooleanField(default=False, blank=True, verbose_name='Утвердждено?')

    class Meta:
        verbose_name = 'Ответ преподователя'
        verbose_name_plural = '6. Ответы преподователей'
        ordering = ['user']

    def __str__(self):
        return f'Ответ {self.user}'

    def get_criteria(self):
        return self.indicator.criteria.name
    # get_criteria.admin_order_field = 'criteria'  #Allows column order sorting
    get_criteria.short_description = 'Критерий оценки эффективности деятельности'
