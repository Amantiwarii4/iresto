# Generated by Django 3.2.6 on 2021-09-04 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0013_products_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='unit',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='products',
            name='unit_price',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='products',
            name='variation',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
