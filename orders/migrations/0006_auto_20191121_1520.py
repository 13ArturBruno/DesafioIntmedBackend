# Generated by Django 2.2.7 on 2019-11-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20191121_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ramMemory',
            field=models.ManyToManyField(blank=True, related_name='ram_memory', to='products.RamMemory', verbose_name='Memória Ram'),
        ),
    ]
