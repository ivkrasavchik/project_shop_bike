# Generated by Django 2.0.7 on 2018-08-13 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_auto_20180812_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Категория клиента',
            new_name='category',
        ),
    ]
