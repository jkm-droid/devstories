# Generated by Django 3.0.4 on 2020-06-24 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0015_auto_20200623_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='StoryViews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('created_on', models.DateField(auto_now_add=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'story', 'value')},
            },
        ),
    ]
