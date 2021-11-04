# Generated by Django 3.2.8 on 2021-10-31 02:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('start_timestamp', models.DateTimeField(blank=True)),
                ('finish_timestamp', models.DateTimeField(blank=True)),
                ('tasks', models.ManyToManyField(to='tasks.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teams.team')),
                ('tournament',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teams.team')),
                ('tournament',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('success', models.BooleanField(verbose_name='Success of the task')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.task')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teams.team')),
                ('tournament',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournaments.tournament')),
            ],
        ),
    ]