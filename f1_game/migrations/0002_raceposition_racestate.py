# Generated by Django 5.1.3 on 2024-12-17 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('f1_game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RacePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('driver_code', models.CharField(max_length=3)),
                ('time_delta', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RaceState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lap', models.IntegerField()),
                ('position', models.IntegerField()),
                ('tire_wear', models.FloatField()),
                ('fuel', models.FloatField()),
            ],
        ),
    ]
