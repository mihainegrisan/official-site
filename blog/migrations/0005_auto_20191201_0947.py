# Generated by Django 2.2.7 on 2019-12-01 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20191127_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
