# Generated by Django 3.0.4 on 2020-06-21 23:34

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_auto_20200620_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
