# Generated by Django 5.0.4 on 2024-05-03 23:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='church_groups',
            field=models.ManyToManyField(related_name='church_groups_set', related_query_name='church_group', through='core.ChurchGroupUser', to='core.churchgroup', verbose_name='Church group'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='accountusergroup',
            name='group',
            field=models.ForeignKey(db_column='id_group', on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_user_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='accountusergroup',
            name='user',
            field=models.ForeignKey(db_column='id_user', on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_user_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', through='account.AccountUserGroup', to='auth.group', verbose_name='Groups'),
        ),
        migrations.AddField(
            model_name='historicalaccountusergroup',
            name='group',
            field=models.ForeignKey(blank=True, db_column='id_group', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auth.group'),
        ),
        migrations.AddField(
            model_name='historicalaccountusergroup',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalaccountusergroup',
            name='user',
            field=models.ForeignKey(blank=True, db_column='id_user', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaluser',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='loggedinuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='modulemenu',
            name='menu',
            field=models.ForeignKey(db_column='id_menu', on_delete=django.db.models.deletion.CASCADE, related_name='module_menus', to='account.menu'),
        ),
        migrations.AddField(
            model_name='modulemenu',
            name='module',
            field=models.ForeignKey(db_column='id_module', on_delete=django.db.models.deletion.CASCADE, related_name='module_menus', to='account.module'),
        ),
        migrations.AddField(
            model_name='modulemenu',
            name='root',
            field=models.ForeignKey(db_column='id_root', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='account.menu'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('username',), name='user_unique_username'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('matriculation',), name='matriculation_unique'),
        ),
        migrations.AlterUniqueTogether(
            name='modulemenu',
            unique_together={('module', 'menu')},
        ),
    ]