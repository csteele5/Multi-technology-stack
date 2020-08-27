# Generated by Django 2.2.15 on 2020-08-20 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20200820_2234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectteam',
            options={'verbose_name_plural': 'Project Teams'},
        ),
        migrations.CreateModel(
            name='SprintPairing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_points', models.IntegerField(default=0)),
                ('completed_points', models.IntegerField(default=0)),
                ('pairing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='schedule.Pairing')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Sprint')),
            ],
        ),
    ]