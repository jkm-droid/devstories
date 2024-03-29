# Generated by Django 3.0.4 on 2020-08-20 23:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0016_auto_20200624_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveForLater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.IntegerField()),
                ('is_saved', models.BooleanField(default=False)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
