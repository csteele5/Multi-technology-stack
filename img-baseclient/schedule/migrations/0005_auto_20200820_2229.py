# Generated by Django 2.2.15 on 2020-08-20 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_sprint'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sprint',
            options={'ordering': ['-sprint_end_date']},
        ),
        migrations.AddField(
            model_name='sprint',
            name='assigned_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sprint',
            name='completed_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sprint',
            name='project_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='schedule.ProjectTeam', verbose_name='Project Team'),
        ),
    ]