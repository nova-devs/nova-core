# Generated by Django 5.0.4 on 2024-05-03 23:13
from django.contrib.postgres.operations import UnaccentExtension

import account.managers
import simple_history.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("CREATE SCHEMA IF NOT EXISTS history"),
        UnaccentExtension(),
        migrations.CreateModel(
            name='GlobalPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_column='tx_username', max_length=16, unique=True, verbose_name='Username')),
                ('password', models.CharField(db_column='tx_password', max_length=104, verbose_name='Password')),
                ('matriculation', models.CharField(db_column='tx_matriculation', max_length=16, null=True, unique=True, verbose_name='Matriculation')),
                ('name', models.CharField(blank=True, db_column='tx_name', default='', max_length=256, verbose_name='Name')),
                ('email', models.CharField(db_column='tx_email', max_length=256, null=True, verbose_name='e-Mail')),
                ('is_active', models.BooleanField(db_column='cs_active', default=True, verbose_name='Is active')),
                ('is_superuser', models.BooleanField(db_column='cs_superuser', default=False, null=True, verbose_name='Is superuser')),
                ('is_staff', models.BooleanField(db_column='cs_staff', default=False, null=True)),
                ('is_default', models.BooleanField(db_column='cs_default', default=False, null=True)),
                ('last_login', models.DateTimeField(db_column='dt_last_login', null=True)),
                ('avatar', models.BinaryField(db_column='bl_avatar', null=True, verbose_name='Avatar')),
                ('phone_number', models.CharField(blank=True, db_column='tx_phone_number', max_length=13, null=True, verbose_name='Phone number')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], db_column='cs_gender', default='M', max_length=1, verbose_name='Gender')),
                ('birthday', models.DateField(db_column='dt_birthday', null=True, verbose_name='Birthday')),
                ('has_access', models.BooleanField(db_column='cs_has_access', default=False)),
            ],
            managers=[
                ('objects', account.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AccountUserGroup',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'account_user_groups',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalAccountUserGroup',
            fields=[
                ('id', models.BigIntegerField(blank=True, db_column='id', db_index=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical account user group',
                'verbose_name_plural': 'historical account user groups',
                'db_table': '"history"."account_user_groups"',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('username', models.CharField(db_column='tx_username', db_index=True, max_length=16, verbose_name='Username')),
                ('password', models.CharField(db_column='tx_password', max_length=104, verbose_name='Password')),
                ('matriculation', models.CharField(db_column='tx_matriculation', db_index=True, max_length=16, null=True, verbose_name='Matriculation')),
                ('name', models.CharField(blank=True, db_column='tx_name', default='', max_length=256, verbose_name='Name')),
                ('email', models.CharField(db_column='tx_email', max_length=256, null=True, verbose_name='e-Mail')),
                ('is_active', models.BooleanField(db_column='cs_active', default=True, verbose_name='Is active')),
                ('is_superuser', models.BooleanField(db_column='cs_superuser', default=False, null=True, verbose_name='Is superuser')),
                ('is_staff', models.BooleanField(db_column='cs_staff', default=False, null=True)),
                ('is_default', models.BooleanField(db_column='cs_default', default=False, null=True)),
                ('last_login', models.DateTimeField(db_column='dt_last_login', null=True)),
                ('avatar', models.BinaryField(db_column='bl_avatar', null=True, verbose_name='Avatar')),
                ('phone_number', models.CharField(blank=True, db_column='tx_phone_number', max_length=13, null=True, verbose_name='Phone number')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], db_column='cs_gender', default='M', max_length=1, verbose_name='Gender')),
                ('birthday', models.DateField(db_column='dt_birthday', null=True, verbose_name='Birthday')),
                ('has_access', models.BooleanField(db_column='cs_has_access', default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical user',
                'verbose_name_plural': 'historical users',
                'db_table': '"history"."user"',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='LoggedInUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_token', models.CharField(blank=True, max_length=10000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='dt_created')),
            ],
            options={
                'db_table': 'account_logged_in_user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, db_column='tx_description', max_length=64, null=True)),
                ('icon', models.CharField(blank=True, db_column='tx_icon', max_length=64, null=True)),
                ('route', models.CharField(blank=True, db_column='tx_route', max_length=64, null=True)),
            ],
            options={
                'db_table': 'account_menu',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, db_column='tx_description', max_length=64, null=True, unique=True)),
                ('icon', models.CharField(blank=True, db_column='tx_icon', max_length=64, null=True)),
                ('is_active', models.BooleanField(db_column='cs_active', default=True)),
            ],
            options={
                'db_table': 'account_module',
                'permissions': (('load_module', 'Can load module'),),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ModuleMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(db_column='nb_order', null=True)),
                ('has_divider', models.BooleanField(db_column='cs_divisor', default=False)),
                ('is_active', models.BooleanField(db_column='cs_active', default=True)),
            ],
            options={
                'db_table': 'account_module_menu',
                'permissions': (('load_module_menu', 'Can load module menu'),),
                'managed': True,
            },
        ),
    ]