# Generated by Django 5.0.4 on 2024-05-15 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_mascota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='mascotas'),
        ),
    ]
