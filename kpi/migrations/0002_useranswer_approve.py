# Generated by Django 4.0.5 on 2022-06-23 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='approve',
            field=models.BooleanField(blank=True, default=False, verbose_name='Утвердждено?'),
        ),
    ]
