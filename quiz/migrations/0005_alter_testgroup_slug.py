# Generated by Django 4.2.1 on 2023-05-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_alter_testgroup_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testgroup',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
