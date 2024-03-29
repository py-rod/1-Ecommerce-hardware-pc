# Generated by Django 5.0 on 2023-12-07 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_alter_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slogan', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ForeignKey(default='', help_text='Select a product to post in the carousel', on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'verbose_name_plural': 'Upload images for carousel',
                'db_table': 'Images_Carousel',
            },
        ),
    ]
