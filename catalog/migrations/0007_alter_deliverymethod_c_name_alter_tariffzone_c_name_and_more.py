# Generated by Django 5.0.1 on 2024-05-30 20:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_deliverymethod_tariffzone_metermeasure'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverymethod',
            name='C_Name',
            field=models.CharField(help_text='Введите источник показания', max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='tariffzone',
            name='C_Name',
            field=models.CharField(help_text='Введите тарифную зону', max_length=200, verbose_name='Наименование'),
        ),
        migrations.CreateModel(
            name='MeterReadings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('N_Value', models.FloatField(verbose_name='Значение')),
                ('D_Date', models.DateField(verbose_name='Дата показания')),
                ('C_Notes', models.TextField(help_text='Примечание', verbose_name='Наименование')),
                ('Img', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Вложение')),
                ('F_Creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('F_Delivery_Methods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.deliverymethod', verbose_name='Источник показания')),
                ('F_Devices', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.device', verbose_name='Прибор')),
                ('F_Division', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.division', verbose_name='Цех')),
                ('F_Tariff_Zones', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.tariffzone', verbose_name='Тарифная зона')),
            ],
        ),
    ]
