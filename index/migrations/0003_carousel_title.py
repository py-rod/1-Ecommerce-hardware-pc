# Generated by Django 5.0 on 2023-12-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_alter_carousel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
