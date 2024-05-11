# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.utils import timezone

from nova import messages


class ModelBase(models.Model):
    id = models.BigAutoField(
        db_column='id',
        null=False,
        primary_key=True,
        verbose_name=_('Id')
    )
    created_at = models.DateTimeField(
        db_column='dt_created',
        auto_now_add=True,
        null=True,
        verbose_name=_('Created at')
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified',
        auto_now=True,
        null=True,
        verbose_name=_('Modified at')
    )
    is_active = models.BooleanField(
        db_column='cs_is_active',
        null=False,
        default=True,
        verbose_name=_('Active'),
    )

    class Meta:
        abstract = True
        managed = True
        default_permissions = ('add', 'change', 'delete', 'view')


class Config(ModelBase):
    class Key(models.TextChoices):
        SMTP_SERVER = 'SMTP_SERVER', _('SMTP server')

    key = models.CharField(
        verbose_name=_('Key'),
        db_column='tx_key',
        max_length=100,
        null=False,
        unique=True,
        choices=Key.choices
    )
    value = models.CharField(
        verbose_name=_('Value'),
        max_length=255,
        db_column='tx_value',
        null=False
    )

    class Meta:
        db_table = 'config'
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')


class ChurchGroup(ModelBase):
    class Type(models.TextChoices):
        SEMINARY = 'SE', messages.SEMINARY
        MINISTRY = 'MI', messages.MINISTRY
        GA = 'GA', messages.GA
        FLOCK = 'FL', messages.FLOCK
        ORIENTATION = 'OR', messages.ORIENTATION
        GENERAL = 'GE', messages.GENERAL

    class Category(models.TextChoices):
        CHURCH = 'CH', messages.CHURCH
        NOVA_BABY = 'NB', messages.NOVA_BABY
        NOVA_INFANTIL = 'NI', messages.NOVA_INFANTIL
        NOVA_KIDS = 'NK', messages.NOVA_KIDS
        NOVA_TEENS = 'NT', messages.NOVA_TEENS
        NOVA_JOVENS = 'NJ', messages.NOVA_JOVENS
        NOVA_MIX = 'NM', messages.NOVA_MIX
        NOVA_CASAIS = 'NC', messages.NOVA_CASAIS
        NOVA_MULHER = 'NW', messages.NOVA_MULHER
        NOVA_IDADE = 'NA', messages.NOVA_IDADE

    description = models.CharField(
        db_column='tx_description',
        max_length=256,
        null=False,
        unique=True,
        verbose_name=messages.DESCRIPTION
    )
    type = models.CharField(
        db_column='cs_type',
        max_length=2,
        null=False,
        choices=Type.choices,
        verbose_name=messages.TYPE
    )
    category = models.CharField(
        db_column='cs_category',
        max_length=2,
        null=False,
        choices=Category.choices,
        verbose_name=messages.CATEGORY
    )

    users = models.ManyToManyField(
        to='account.User',
        through='ChurchGroupUser',
        verbose_name=messages.USERS,
        related_name='users_set',
        related_query_name='user'
    )
    history = HistoricalRecords(table_name='"history"."church_group"')

    class Meta:
        db_table = '"core"."church_group"'
        verbose_name = messages.CHURCH_GROUP
        verbose_name_plural = messages.CHURCH_GROUPS


class ChurchGroupUser(ModelBase):
    class AssociationType(models.TextChoices):
        PRINCIPAL_LEADER = 'P', messages.PRINCIPAL_LEADER
        AUXILIARY_LEADER = 'A', messages.AUXILIARY_LEADER
        MEMBER = 'M', messages.MEMBER

    user = models.ForeignKey(
        db_column='id_user',
        to='account.User',
        null=False,
        on_delete=models.DO_NOTHING,
        verbose_name=messages.USER
    )
    church_group = models.ForeignKey(
        db_column='id_church_group',
        to='ChurchGroup',
        null=False,
        on_delete=models.DO_NOTHING,
        verbose_name=messages.CHURCH_GROUP
    )
    association_type = models.CharField(
        db_column='cs_association_type',
        max_length=1,
        null=False,
        default=AssociationType.MEMBER,
        choices=AssociationType.choices,
        verbose_name=messages.ASSOCIATION_TYPE
    )
    history = HistoricalRecords(table_name='"history"."church_group_user"')

    class Meta:
        db_table = '"core"."church_group_user"'
        unique_together = [['user', 'church_group']]
        verbose_name = messages.CHURCH_GROUP_USER
        verbose_name_plural = messages.CHURCH_GROUP_USERS
