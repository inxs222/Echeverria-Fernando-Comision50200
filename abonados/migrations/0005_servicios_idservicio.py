# Generated by Django 5.0.1 on 2024-02-12 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abonados', '0004_alter_facturas_date_alter_facturas_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicios',
            name='idServicio',
            field=models.IntegerField(default=0),
        ),
    ]
