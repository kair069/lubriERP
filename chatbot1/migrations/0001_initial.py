# Generated by Django 5.1.1 on 2025-02-22 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=255)),
                ('texto', models.TextField()),
                ('respuesta', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('producto_relacionado', models.CharField(blank=True, max_length=255, null=True)),
                ('demanda_estimada', models.IntegerField(blank=True, null=True)),
                ('stock_actual', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
