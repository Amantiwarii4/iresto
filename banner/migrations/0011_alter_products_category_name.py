# Generated by Django 3.2.6 on 2021-09-04 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0010_rename_category_name_banner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='banner.category'),
        ),
    ]
