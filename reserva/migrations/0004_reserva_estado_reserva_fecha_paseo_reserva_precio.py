# Generated by Django 5.0.4 on 2024-05-27 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0003_alter_reserva_mascota'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='estado',
            field=models.CharField(choices=[('rechazada', 'Rechazada'), ('pendiente', 'Pendiente'), ('aceptada', 'Aceptada')], default='pendiente', max_length=20),
        ),
        migrations.AddField(
            model_name='reserva',
            name='fecha_paseo',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='precio',
            field=models.IntegerField(null=True),
        ),
    ]
