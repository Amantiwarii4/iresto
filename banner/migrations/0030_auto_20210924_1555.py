# Generated by Django 3.2.6 on 2021-09-24 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banner', '0029_orders_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dine_in',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_tables', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('status', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='orders',
            name='type',
        ),
        migrations.AddField(
            model_name='products',
            name='unit_price_admin',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(blank=True, default='Order Confirmed', max_length=200),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, default='Booked', max_length=200)),
                ('date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
