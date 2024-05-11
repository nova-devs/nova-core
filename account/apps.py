from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        import account.receivers  # noqa: F401
        super().ready()
