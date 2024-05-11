import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from django.contrib.auth import models as auth_models
from django.db import transaction
from django.db.models import Q
from guardian import shortcuts

from account import exceptions, helpers, models, queries


def identity(user: int = None, group: int = None):
    _user, _group = None, None
    if user:
        _user = models.User.objects.filter(id=user).first()
    if group:
        _group = auth_models.Group.objects.filter(id=group).first()

    return _user, _group


def decrypt_string(text):
    enc = base64.b64decode(text)
    derived_key = base64.b64decode("LefjQ2pEXmiy/nNZvEJ43i8hJuaAnzbA1Cbn1hOuAgA=")
    iv = "1020304050607080"
    cipher = AES.new(derived_key, AES.MODE_CBC, iv.encode('utf-8'))
    return unpad(cipher.decrypt(enc), 16).decode('utf-8')


def grant_group_to_user(group, user: int, granted: bool):
    _user = queries.get_user_by_id(pk=user)
    if not _user:
        return

    if granted:
        _user.groups.add(group)
    else:
        _user.groups.remove(group)


def grant_menu_to_user_or_group(menu, granted: bool, user: int = None, group: int = None):
    if user:
        user_or_group = queries.get_user_by_id(pk=user)
    else:
        user_or_group = queries.get_group_by_id(pk=group)

    if not user_or_group:
        return

    if granted:
        shortcuts.assign_perm('load_menu', user_or_group, menu)
    else:
        shortcuts.remove_perm('load_menu', user_or_group, menu)


@transaction.atomic
def grant_all_menu_to_user_or_group(queryset, granted: bool, user: int = None, group: int = None):
    if user:
        user_or_group = queries.get_user_by_id(pk=user)
    else:
        user_or_group = queries.get_group_by_id(pk=group)

    if not user_or_group:
        return

    for menu in queryset:
        if granted:
            shortcuts.assign_perm('load_menu', user_or_group, menu)
        else:
            shortcuts.remove_perm('load_menu', user_or_group, menu)


def grant_permission_to_user_or_group(permission, granted: bool, user: int = None, group: int = None):
    if user:
        user_or_group = queries.get_user_by_id(pk=user)
    else:
        user_or_group = queries.get_group_by_id(pk=group)

    if not user_or_group:
        return

    user, group = helpers.get_identity(user_or_group)
    if user:
        if granted:
            user.user_permissions.add(permission)
        else:
            user.user_permissions.remove(permission)

    if group:
        if granted:
            group.permissions.add(permission)
        else:
            group.permissions.remove(permission)


@transaction.atomic
def grant_all_permission_to_user_or_group(queryset, granted: bool, user: int = None, group: int = None):
    if user:
        user_or_group = queries.get_user_by_id(pk=user)
    else:
        user_or_group = queries.get_group_by_id(pk=group)

    if not user_or_group:
        return

    for permission in queryset:
        user, group = helpers.get_identity(user_or_group)
        if user:
            if granted:
                user.user_permissions.add(permission)
            else:
                user.user_permissions.remove(permission)

        if group:
            if granted:
                group.permissions.add(permission)
            else:
                group.permissions.remove(permission)


class UserActions:
    @staticmethod
    def change_password(instance: 'models.User', password: str = None, new_password: str = None, reset: bool = False):
        if not reset and not instance.check_password(raw_password=password):
            raise exceptions.InvalidPasswordException

        if new_password:
            instance.set_password(raw_password=new_password)
            instance.save()

    @staticmethod
    @transaction.atomic
    def associate_to_group(queryset, source: int = None, target: int = None, associated: bool = False):
        def _associate(_source: int):
            instance = models.User.objects.get(pk=_source)
            if associated:
                models.AccountUserGroup(
                    user=instance,
                    group=auth_models.Group.objects.get(pk=target)
                ).save()
            else:
                instance.groups.remove(target)

        if source > 0:
            _associate(_source=source)
        else:
            for u in queryset.values('id'):
                _associate(_source=u['id'])

    @staticmethod
    def recovery_password(username: str):
        pass
        # user = models.User.objects.filter(username=username)
        #
        # email_params = obtains_params()
        # if user:
        #     if user.email:
        #         pwd_temp = utils.password_random()
        #         user.set_password(raw_password=pwd_temp)
        #         user.save()
        #         send_mail_message(
        #             to=[user.email],
        #             password_temp=pwd_temp,
        #             emails_params=email_params
        #         )
        #         return {'detail': messages.EMAIL_SUCCESSFULLY_SENT}
        #     else:
        #         raise exceptions.IncompleteEmailUserException
        # else:
        #     raise exceptions.InvalidUserException

    @staticmethod
    def send_mail_message(to: [], password_temp, emails_params: dict):
        pass
        # subject = 'Recuperação de senha'
        #
        # with open('account/html/recovery_email.html') as body:
        #     try:
        #         connection = EmailBackend(
        #             host=emails_params['host'],
        #             port=emails_params['port'],
        #             username=emails_params['sender'],
        #             password=emails_params['password'],
        #             use_tls=util.strtobool(emails_params['use_tls']),
        #             use_ssl=util.strtobool(emails_params['use_ssl']),
        #             fail_silently=False
        #         )
        #         email = EmailMessage(
        #             subject=subject,
        #             body=body.read(),
        #             to=to,
        #             connection=connection
        #         )
        #         email.body = email.body.format(password_temp=password_temp)
        #         email.content_subtype = 'html'
        #         email.send()
        #
        #     except Exception:
        #         raise exceptions.ErrorToSendEmailException()


class GroupActions:
    @staticmethod
    def grant(objects: list, user: int = None, granted: bool = False):
        _user, _ = identity(user=user)
        for obj in objects:
            if granted:
                models.AccountUserGroup(user=_user, group=obj).save()
            else:
                _user.groups.remove(obj)


class PermissionActions:
    @staticmethod
    @transaction.atomic
    def grant(objects: list, permission: str = None, user: int = None, group: int = None, granted: bool = False):
        _user, _group = identity(user=user, group=group)

        for obj in objects:
            if permission:
                user_or_group = _user if _user else _group
                if granted:
                    shortcuts.assign_perm(permission, user_or_group, obj)
                else:
                    shortcuts.remove_perm(permission, user_or_group, obj)
            else:
                _permissions = _user.user_permissions if _user else _group.permissions
                if granted:
                    _permissions.add(obj)
                else:
                    _permissions.remove(obj)


class ModuleMenuActions:
    @staticmethod
    def representation(user: int, module: str):
        response = dict()
        results = dict()
        routes = set()

        # get the menu filtered by user and module
        queryset = queries.ModuleMenuQuerySet()
        menus = queryset.available(user=user, module=module)
        for menu in menus:

            # get the menu root and group by it
            root = menu.get('root__description')

            # create new root if not exists
            if root is not None and root not in results:
                results[root] = {
                    'label': root,
                    'hidden': False,
                    'items': []
                }

            if root is not None:
                # add item to root of menu
                data = {
                    'icon': menu.get('menu__icon'),
                    'label': menu.get('menu__description'),
                    'route': menu.get('menu__route'),
                    'divider': menu.get('has_divider'),
                    'hidden': not menu.get('is_active'),
                }

                results[root]['items'].append(data)
                # add menu route to set collection
                routes.add(menu.get('menu__route'))

        # generate response
        response['routes'] = list(routes)
        response['results'] = list(results.values())

        return response

    @staticmethod
    def order_on_create(module: 'models.Module'):
        order = 1
        item = module.module_menus.order_by('order')
        if item:
            order = item.last().order + 1
        return order

    @staticmethod
    def order_on_delete(item: 'models.ModuleMenu'):
        next_item = item.module.module_menus.filter(
            order__gt=item.order
        ).order_by('order')

        if next_item.exists():
            order = item.order
            for procedure_item in next_item:
                procedure_item.order = order
                procedure_item.save()
                order += 1

    @staticmethod
    def order_on_update(item: 'models.ModuleMenu', item_to_move: 'models.ModuleMenu'):
        if item_to_move.order > item.order:
            filters = Q(order__gte=item.order) & Q(
                order__lte=item_to_move.order)
            asc = True
        else:
            filters = Q(order__gte=item_to_move.order) & Q(
                order__lte=item.order)
            asc = False

        items = item.module.module_menus.filter(filters)

        if items.exists():
            for procedure_item in items:
                procedure_item.order = procedure_item.order + 1 if asc else procedure_item.order - 1
                procedure_item.save()

        item_to_move.order = item.order
        item_to_move.save()
