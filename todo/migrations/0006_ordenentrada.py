# Generated by Django 5.1.6 on 2025-04-11 00:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_proveedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenEntrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_orden', models.DateField(auto_now_add=True)),
                ('descripcion', models.TextField(blank=True)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.proveedor')),
            ],
        ),
    ]
