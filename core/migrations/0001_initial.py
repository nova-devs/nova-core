# Generated by Django 5.0.4 on 2024-05-03 23:13

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL("CREATE SCHEMA IF NOT EXISTS core"),
        migrations.CreateModel(
            name='ChurchGroup',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='dt_created', null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_column='dt_modified', null=True, verbose_name='Modified at')),
                ('active', models.BooleanField(db_column='cs_active', default=True, verbose_name='Active')),
                ('description', models.CharField(db_column='tx_description', max_length=256, unique=True, verbose_name='Description')),
                ('type', models.CharField(choices=[('SE', 'Seminary'), ('MI', 'Ministry'), ('GA', 'GA'), ('FL', 'Flock'), ('OR', 'Orientation'), ('GE', 'General')], db_column='cs_type', max_length=2, verbose_name='Type')),
                ('category',
                 models.CharField(choices=[('CH', 'Church'), ('NB', 'Nova Baby'), ('NI', 'Nova Childish'), ('NK', 'Nova Kids'), ('NT', 'Nova Teens'), ('NJ', 'Nova Youth'), ('NM', 'Nova Mix'), ('NC', 'Nova Couple'), ('NW', 'Nova Mulher'), ('NA', 'Nova Idade')], db_column='cs_category', max_length=2,
                                  verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Church group',
                'verbose_name_plural': 'Church groups',
                'db_table': '"core"."church_group"',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='dt_created', null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_column='dt_modified', null=True, verbose_name='Modified at')),
                ('active', models.BooleanField(db_column='cs_active', default=True, verbose_name='Active')),
                ('key', models.CharField(
                    choices=[('INITIAL_POSITION_OF_PART_NUMBER_ON_SERIAL', 'Initial position of part number on serial'), ('FINAL_POSITION_OF_PART_NUMBER_ON_SERIAL', 'Final position of part number on serial'), ('INITIAL_POSITION_OF_ANGLER_READ_ON_SERIAL', 'Initial position of angle read on serial'),
                             ('FINAL_POSITION_OF_ANGLER_READ_ON_SERIAL', 'Final position of angle read on serial')], db_column='tx_key', max_length=100, unique=True, verbose_name='Key')),
                ('value', models.CharField(db_column='tx_value', max_length=255, verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
                'db_table': 'config',
            },
        ),
        migrations.CreateModel(
            name='ChurchGroupUser',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='dt_created', null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, db_column='dt_modified', null=True, verbose_name='Modified at')),
                ('active', models.BooleanField(db_column='cs_active', default=True, verbose_name='Active')),
                ('association_type', models.CharField(choices=[('P', 'Principal leader'), ('A', 'Auxiliary leader'), ('M', 'Member')], db_column='cs_association_type', default='M', max_length=1, verbose_name='Association type')),
                ('church_group', models.ForeignKey(db_column='id_church_group', on_delete=django.db.models.deletion.DO_NOTHING, to='core.churchgroup', verbose_name='Church group')),
                ('user', models.ForeignKey(db_column='id_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Church group user',
                'verbose_name_plural': 'Church group users',
                'db_table': '"core"."church_group_user"',
                'unique_together': {('user', 'church_group')},
            },
        ),
        migrations.AddField(
            model_name='churchgroup',
            name='users',
            field=models.ManyToManyField(related_name='users_set', related_query_name='user', through='core.ChurchGroupUser', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
        migrations.CreateModel(
            name='HistoricalChurchGroup',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_column='id', db_index=True, verbose_name='Id')),
                ('created_at', models.DateTimeField(blank=True, db_column='dt_created', editable=False, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(blank=True, db_column='dt_modified', editable=False, null=True, verbose_name='Modified at')),
                ('active', models.BooleanField(db_column='cs_active', default=True, verbose_name='Active')),
                ('description', models.CharField(db_column='tx_description', db_index=True, max_length=256, verbose_name='Description')),
                ('type', models.CharField(choices=[('SE', 'Seminary'), ('MI', 'Ministry'), ('GA', 'GA'), ('FL', 'Flock'), ('OR', 'Orientation'), ('GE', 'General')], db_column='cs_type', max_length=2, verbose_name='Type')),
                ('category',
                 models.CharField(choices=[('CH', 'Church'), ('NB', 'Nova Baby'), ('NI', 'Nova Childish'), ('NK', 'Nova Kids'), ('NT', 'Nova Teens'), ('NJ', 'Nova Youth'), ('NM', 'Nova Mix'), ('NC', 'Nova Couple'), ('NW', 'Nova Mulher'), ('NA', 'Nova Idade')], db_column='cs_category', max_length=2,
                                  verbose_name='Category')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Church group',
                'verbose_name_plural': 'historical Church groups',
                'db_table': '"history"."church_group"',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalChurchGroupUser',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_column='id', db_index=True, verbose_name='Id')),
                ('created_at', models.DateTimeField(blank=True, db_column='dt_created', editable=False, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(blank=True, db_column='dt_modified', editable=False, null=True, verbose_name='Modified at')),
                ('active', models.BooleanField(db_column='cs_active', default=True, verbose_name='Active')),
                ('association_type', models.CharField(choices=[('P', 'Principal leader'), ('A', 'Auxiliary leader'), ('M', 'Member')], db_column='cs_association_type', default='M', max_length=1, verbose_name='Association type')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('church_group', models.ForeignKey(blank=True, db_column='id_church_group', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.churchgroup', verbose_name='Church group')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_column='id_user', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'historical Church group user',
                'verbose_name_plural': 'historical Church group users',
                'db_table': '"history"."church_group_user"',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
