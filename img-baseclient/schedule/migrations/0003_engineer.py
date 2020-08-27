# Generated by Django 2.2.15 on 2020-08-20 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_projectteam_team_lead'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('available_for_sprint', models.BooleanField(default=True)),
                ('avg_team_points_assigned', models.IntegerField(default=0)),
                ('avg_team_points_completed', models.IntegerField(default=0)),
                ('project_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='schedule.ProjectTeam', verbose_name='Project Team')),
            ],
        ),
    ]