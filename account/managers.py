from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Exists, OuterRef


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, name, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_user(self, username, name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_default', False)
        return self._create_user(username, name, password, **extra_fields)

    def create_superuser(self, username, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_default', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, name, password, **extra_fields)

    def associated(self, group: int):
        subquery = self.filter(
            id=OuterRef('pk'),
            groups=group
        ).values('id')
        return self.annotate(
            associated=Exists(subquery)
        )
