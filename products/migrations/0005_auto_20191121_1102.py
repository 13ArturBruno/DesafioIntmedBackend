# Generated by Django 2.2.7 on 2019-11-21 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20191121_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motherboard',
            name='cpuSupport',
            field=models.ManyToManyField(related_name='cpu_support', to='products.Brand', verbose_name='Processadores Suportados'),
        ),
    ]