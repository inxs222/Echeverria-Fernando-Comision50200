# Generated by Django 5.0.1 on 2024-01-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abonados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nAbonado', models.IntegerField()),
                ('servicio', models.CharField(max_length=250)),
                ('servicioMonto', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='facturas',
            name='pago',
            field=models.CharField(default='no', max_length=2),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='date',
            field=models.IntegerField(),
        ),
    ]
