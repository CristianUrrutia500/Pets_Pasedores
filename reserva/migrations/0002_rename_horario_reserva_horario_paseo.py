# Generated by Django 5.0.4 on 2024-05-24 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserva',
            old_name='horario',
            new_name='horario_paseo',
        ),
    ]
