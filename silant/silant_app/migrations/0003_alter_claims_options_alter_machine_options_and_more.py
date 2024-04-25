# Generated by Django 5.0.3 on 2024-04-24 10:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silant_app', '0002_alter_claims_options_alter_controlledaxle_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='claims',
            options={'ordering': ['equipment_failure_date'], 'verbose_name': 'Рекламация', 'verbose_name_plural': 'Рекламации'},
        ),
        migrations.AlterModelOptions(
            name='machine',
            options={'ordering': ['factory_shipment_date'], 'verbose_name': 'Машина', 'verbose_name_plural': 'Машины'},
        ),
        migrations.AlterModelOptions(
            name='maintenance',
            options={'ordering': ['maintenance_date'], 'verbose_name': 'Техническое обслуживание', 'verbose_name_plural': 'Технические обслуживания'},
        ),
        migrations.AlterField(
            model_name='machine',
            name='controlled_axle_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machines', to='silant_app.controlledaxle', verbose_name='Модель управляемого моста'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='driving_axle_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machines', to='silant_app.drivingaxle', verbose_name='Модель ведущего моста'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='engine_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machines', to='silant_app.engine', verbose_name='Модель двигателя'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='machine_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machines', to='silant_app.machinemodel', verbose_name='Модель техники'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='transmission_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machines', to='silant_app.transmission', verbose_name='Модель трансмиссии'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_service', models.BooleanField(blank=True, default=False, verbose_name='Является сотрудником сервисной компании')),
                ('service_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='silant_app.servicecompany', verbose_name='Сервисная компания')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
