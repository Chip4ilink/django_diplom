# Generated by Django 5.0.1 on 2024-05-31 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_rename_meterreadings_meterreading'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meterreading',
            options={'ordering': ['F_Division', 'D_Date']},
        ),
        migrations.AddField(
            model_name='division',
            name='C_Notes',
            field=models.TextField(null=True, verbose_name='Примечание'),
        ),
    ]
