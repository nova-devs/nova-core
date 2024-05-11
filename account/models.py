from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group as DjangoGroup
from django.db import models
from django.db.models import UniqueConstraint
from simple_history.models import HistoricalRecords

from account import managers
from nova import messages


class GlobalPermissions(models.Model):
    class Meta:
        managed = False
        permissions = (
        )


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = ('M', messages.MALE)
        FEMALE = ('F', messages.FEMALE)

    username = models.CharField(
        db_column='tx_username',
        null=False,
        max_length=16,
        unique=True,
        verbose_name=messages.USERNAME
    )
    password = models.CharField(
        db_column='tx_password',
        null=False,
        max_length=104,
        verbose_name=messages.PASSWORD
    )
    matriculation = models.CharField(
        db_column='tx_matriculation',
        null=True,
        max_length=16,
        unique=True,
        verbose_name=messages.MATRICULATION
    )
    name = models.CharField(
        db_column='tx_name',
        null=False,
        blank=True,
        max_length=256,
        default="",
        verbose_name=messages.NAME
    )
    email = models.CharField(
        db_column='tx_email',
        null=True,
        max_length=256,
        verbose_name=messages.EMAIL
    )
    is_active = models.BooleanField(
        db_column='cs_active',
        null=False,
        default=True,
        verbose_name=messages.IS_ACTIVE
    )
    is_superuser = models.BooleanField(
        db_column='cs_superuser',
        null=True,
        default=False,
        verbose_name=messages.IS_SUPERUSER
    )
    is_staff = models.BooleanField(
        db_column='cs_staff',
        null=True,
        default=False
    )
    is_default = models.BooleanField(
        db_column='cs_default',
        null=True,
        default=False
    )
    last_login = models.DateTimeField(
        db_column='dt_last_login',
        null=True
    )
    avatar = models.BinaryField(
        db_column='bl_avatar',
        null=True,
        verbose_name=messages.AVATAR
    )
    phone_number = models.CharField(
        db_column='tx_phone_number',
        null=True,
        blank=True,
        max_length=13,
        verbose_name=messages.PHONE_NUMBER
    )
    gender = models.CharField(
        db_column="cs_gender",
        null=False,
        max_length=1,
        default=Gender.MALE,
        choices=Gender.choices,
        verbose_name=messages.GENDER
    )
    birthday = models.DateField(
        db_column='dt_birthday',
        null=True,
        verbose_name=messages.BIRTHDAY
    )
    has_access = models.BooleanField(
        db_column='cs_has_access',
        null=False,
        default=False
    )

    church_groups = models.ManyToManyField(
        to='core.ChurchGroup',
        through='core.ChurchGroupUser',
        verbose_name=messages.CHURCH_GROUP,
        related_name='church_groups_set',
        related_query_name='church_group'
    )

    groups = models.ManyToManyField(
        to=DjangoGroup,
        through='AccountUserGroup',
        verbose_name=messages.GROUPS,
        blank=True,
        help_text=messages.USER_GROUPS_HELP_TEXT,
        related_name="user_set",
        related_query_name="user",
    )

    objects = managers.UserManager()
    history = HistoricalRecords(table_name='"history"."user"')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    # def get_absolute_url(self):
    #     return reverse('user-detail', kwargs={'pk': self.id})

    class Meta:
        constraints = [
            UniqueConstraint(fields=['username'], name='user_unique_username'),
            UniqueConstraint(fields=['matriculation'], name='matriculation_unique')
        ]


class AccountUserGroup(models.Model):
    id = models.BigAutoField(
        db_column='id',
        primary_key=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='id_user',
        related_name='account_user_groups',
    )
    group = models.ForeignKey(
        DjangoGroup,
        on_delete=models.DO_NOTHING,
        db_column='id_group',
        related_name='account_user_groups',
    )

    history = HistoricalRecords(table_name='"history"."account_user_groups"')

    class Meta:
        managed = True
        db_table = 'account_user_groups'


class Module(models.Model):
    id = models.BigAutoField(
        db_column='id',
        primary_key=True
    )
    description = models.CharField(
        db_column='tx_description',
        max_length=64,
        unique=True,
        blank=True,
        null=True,
    )
    icon = models.CharField(
        db_column='tx_icon',
        max_length=64,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        db_column='cs_active',
        null=False,
        default=True,
    )

    def __str__(self):
        return self.description

    class Meta:
        managed = True
        db_table = 'account_module'
        permissions = (
            ('load_module', 'Can load module'),
        )


class Menu(models.Model):
    id = models.BigAutoField(
        db_column='id',
        primary_key=True
    )
    description = models.CharField(
        db_column='tx_description',
        max_length=64,
        blank=True,
        null=True,
    )
    icon = models.CharField(
        db_column='tx_icon',
        max_length=64,
        blank=True,
        null=True,
    )
    route = models.CharField(
        db_column='tx_route',
        max_length=64,
        blank=True,
        null=True,
    )

    def __str__(self):
        return '%s - %s' % (self.description, self.route)

    class Meta:
        managed = True
        db_table = 'account_menu'


class ModuleMenu(models.Model):
    root = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        db_column='id_root',
        related_name='menus',
        null=True,
    )
    module = models.ForeignKey(
        'Module',
        on_delete=models.CASCADE,
        db_column='id_module',
        related_name='module_menus',
        null=False,
    )
    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        db_column='id_menu',
        related_name='module_menus',
        null=False,
    )
    order = models.IntegerField(
        db_column='nb_order',
        null=True,
    )
    has_divider = models.BooleanField(
        db_column='cs_divisor',
        null=False,
        default=False,
    )
    is_active = models.BooleanField(
        db_column='cs_active',
        null=False,
        default=True,
    )

    def __str__(self):
        return '%s - %s' % (self.module.description, self.menu.description)

    class Meta:
        managed = True
        db_table = 'account_module_menu'
        unique_together = (['module', 'menu'])
        permissions = (
            ('load_module_menu', 'Can load module menu'),
        )


class LoggedInUser(models.Model):
    user = models.ForeignKey(User, related_name="logged_in_user", on_delete=models.CASCADE)
    last_token = models.CharField(max_length=10000, null=True, blank=True)
    created_at = models.DateTimeField(
        db_column="dt_created",
        auto_now_add=True,
        null=False,
    )

    class Meta:
        managed = True
        db_table = 'account_logged_in_user'

    def __str__(self):
        return self.user.username
