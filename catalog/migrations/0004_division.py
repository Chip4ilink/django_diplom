# Generated by Django 5.0.1 on 2024-05-26 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_bookinstance_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('C_Name', models.CharField(max_length=100)),
                ('D_Date_Begin', models.DateField(blank=True, null=True)),
                ('D_Date_End', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
