from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Executa makemigrations seguido de migrate para todos os apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            help='Especifica um nome para a migração',
            default=''
        )

    def handle(self, *args, **options):
        name = options['name']
        self.stdout.write(self.style.SUCCESS('Iniciando makemigrations e migrate...'))

        if name:
            call_command('makemigrations', name=name)
        else:
            call_command('makemigrations')

        call_command('migrate')

        self.stdout.write(self.style.SUCCESS('Migrações criadas e aplicadas com sucesso!'))
