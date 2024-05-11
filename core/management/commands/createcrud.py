import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Automatically creates CRUD operations files for a specified model in a specified app.'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='The Django application name.')
        parser.add_argument('model_name', type=str, help='The model name for which CRUD will be created.')

    def handle(self, *args, **options):
        app_name = options['app_name']
        model_name = options['model_name']
        app_config = f'{app_name}.apps.{app_name.capitalize()}Config'

        if app_config not in settings.INSTALLED_APPS:
            raise CommandError(f'{app_name} is not a valid app or is not configured correctly in INSTALLED_APPS.')

        models_path = os.path.join(app_name, 'models.py')
        serializers_path = os.path.join(app_name, 'serializers.py')
        filters_path = os.path.join(app_name, 'filters.py')
        viewsets_path = os.path.join(app_name, 'viewsets.py')
        urls_path = os.path.join(app_name, 'urls.py')

        if not self.model_exists(models_path, model_name):
            raise CommandError(f'Model "{model_name}" does not exist in {app_name}/models.py')

        self.create_serializer(serializers_path, model_name)
        self.create_filter(filters_path, model_name)
        self.create_viewset(viewsets_path, model_name)
        self.add_route(urls_path, model_name)

        self.stdout.write(self.style.SUCCESS(f'Successfully created CRUD for {model_name} in {app_name}'))

    @staticmethod
    def model_exists(file_path, class_name):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return bool(re.search(r'class\s+' + re.escape(class_name) + r'\s*\(', content))
        except FileNotFoundError:
            return False

    def create_serializer(self, file_path, class_name):
        serializer_class_name = f'{class_name}Serializer'
        serializer_code = f"""

class {serializer_class_name}(SerializerBase):
    class Meta:
        model = models.{class_name}
        fields = '__all__'
"""
        try:
            with open(file_path, 'r+') as file:
                content = file.read()
                if re.search(f'class\\s+{serializer_class_name}\\s*\\(', content):
                    self.stdout.write(self.style.WARNING(f'Serializer "{serializer_class_name}" already exists in {file_path}. Skipping.'))
                else:
                    file.write(serializer_code)
                    self.stdout.write(self.style.SUCCESS(f'Added "{serializer_class_name}" to {file_path}.'))
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('File serializers.py not found. Skipping.'))

    def create_filter(self, file_path, class_name):
        filter_class_name = f'{class_name}Filter'
        filter_code = f"""

class {filter_class_name}(filterset.FilterSet):
    class Meta:
        model = models.{class_name}
        fields = []
"""
        try:
            with open(file_path, 'r+') as file:
                content = file.read()
                if re.search(f'class\\s+{filter_class_name}\\s*\\(', content):
                    self.stdout.write(self.style.WARNING(f'Filter "{filter_class_name}" already exists in {file_path}. Skipping.'))
                else:
                    file.write(filter_code)
                    self.stdout.write(self.style.SUCCESS(f'Added "{filter_class_name}" to {file_path}.'))
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('File filters.py not found. Skipping.'))

    def create_viewset(self, file_path, class_name):
        viewset_class_name = f'{class_name}ViewSet'
        viewset_code = f"""

class {viewset_class_name}(ViewSetBase):
    queryset = models.{class_name}.objects.all()
    serializer_class = serializers.{class_name}Serializer
    filterset_class = filters.{class_name}Filter
    ordering_fields = '__all__'
    ordering = ('-id',)
"""
        try:
            with open(file_path, 'r+') as file:
                content = file.read()
                if re.search(f'class\\s+{viewset_class_name}\\s*\\(', content):
                    self.stdout.write(self.style.WARNING(f'ViewSet "{viewset_class_name}" already exists in {file_path}. Skipping.'))
                else:
                    file.write(viewset_code)
                    self.stdout.write(self.style.SUCCESS(f'Added "{viewset_class_name}" to {file_path}.'))
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('File viewsets.py not found. Skipping.'))

    @staticmethod
    def camel_to_snake(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def add_route(self, file_path, class_name):
        route_name = self.camel_to_snake(class_name)
        route_line = f"router.register('{route_name}', viewset=viewsets.{class_name}ViewSet)\n"
        try:
            with open(file_path, 'r+') as file:
                lines = file.readlines()
                if any(route_line.strip() in line for line in lines):
                    self.stdout.write(self.style.WARNING(f'Route for "{class_name}" already exists in {file_path}. Skipping.'))
                else:
                    lines.insert(-1, route_line)
                    file.seek(0)
                    file.writelines(lines)
                    self.stdout.write(self.style.SUCCESS(f'Added route for "{class_name}" to {file_path}.'))
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f'File {file_path} not found. Skipping.'))
