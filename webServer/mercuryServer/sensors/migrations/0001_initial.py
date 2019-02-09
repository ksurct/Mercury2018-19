# Generated by Django 2.1.2 on 2019-02-09 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qfl', models.DecimalField(decimal_places=15, default=0, max_digits=20)),
                ('qfr', models.DecimalField(decimal_places=15, default=0, max_digits=20)),
                ('qbl', models.DecimalField(decimal_places=15, default=0, max_digits=20)),
                ('qbr', models.DecimalField(decimal_places=15, default=0, max_digits=20)),
                ('df', models.DecimalField(decimal_places=15, default=0, max_digits=20)),
                ('db', models.DecimalField(decimal_places=15, default=0, max_digits=20)),
                ('dl', models.DecimalField(decimal_places=15, default=0, max_digits=20)),
                ('dr', models.DecimalField(decimal_places=15, default=0, max_digits=20)),
            ],
        ),
    ]
