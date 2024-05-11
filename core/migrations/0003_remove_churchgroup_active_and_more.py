# Generated by Django 5.0.4 on 2024-05-19 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_config_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='churchgroup',
            name='active',
        ),
        migrations.RemoveField(
            model_name='churchgroupuser',
            name='active',
        ),
        migrations.RemoveField(
            model_name='config',
            name='active',
        ),
        migrations.RemoveField(
            model_name='historicalchurchgroup',
            name='active',
        ),
        migrations.RemoveField(
            model_name='historicalchurchgroupuser',
            name='active',
        ),
        migrations.AddField(
            model_name='churchgroup',
            name='is_active',
            field=models.BooleanField(db_column='cs_is_active', default=True, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='churchgroupuser',
            name='is_active',
            field=models.BooleanField(db_column='cs_is_active', default=True, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='config',
            name='is_active',
            field=models.BooleanField(db_column='cs_is_active', default=True, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='historicalchurchgroup',
            name='is_active',
            field=models.BooleanField(db_column='cs_is_active', default=True, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='historicalchurchgroupuser',
            name='is_active',
            field=models.BooleanField(db_column='cs_is_active', default=True, verbose_name='Active'),
        ),
    ]