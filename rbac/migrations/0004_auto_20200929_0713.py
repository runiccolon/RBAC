# Generated by Django 3.1.1 on 2020-09-29 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20200929_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
