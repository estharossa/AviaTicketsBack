# Generated by Django 3.2 on 2021-05-10 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankcard',
            name='card_number',
            field=models.CharField(max_length=255, unique=True, verbose_name='Номер карты'),
        ),
    ]
