# Generated by Django 3.0 on 2019-12-26 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20191224_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='ref_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
