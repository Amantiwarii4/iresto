# Generated by Django 3.2.6 on 2021-09-18 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0026_auto_20210918_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='banner.address'),
        ),
        migrations.AddField(
            model_name='orders',
            name='order_type',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
