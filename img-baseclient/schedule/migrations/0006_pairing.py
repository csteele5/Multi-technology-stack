# Generated by Django 2.2.15 on 2020-08-20 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20200820_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pairing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sprint_pairings', models.IntegerField(default=0)),
                ('avg_assigned_points', models.IntegerField(default=0)),
                ('avg_completed_points', models.IntegerField(default=0)),
                ('member1', models.ForeignKey(limit_choices_to={'available_for_sprint': True}, on_delete=django.db.models.deletion.PROTECT, related_name='team_member_a', to='schedule.Engineer', verbose_name='Team Member A')),
                ('member2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='team_member_b', to='schedule.Engineer', verbose_name='Team Member B')),
            ],
            options={
                'verbose_name_plural': 'Engineer Pairings',
            },
        ),
    ]
