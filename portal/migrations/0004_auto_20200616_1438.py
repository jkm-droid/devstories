# Generated by Django 3.0.4 on 2020-06-16 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20200616_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=models.SlugField(max_length=250),
        ),
    ]