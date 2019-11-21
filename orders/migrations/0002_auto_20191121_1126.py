# Generated by Django 2.2.7 on 2019-11-21 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='processor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='processor', to='products.Processor', verbose_name='Processador'),
        ),
    ]
