from django.utils import timezone
from rest_framework.fields import CharField, DateTimeField


class DateTimeFieldWithTZ(DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super().to_representation(value)


class NullCharField(CharField):
    def to_representation(self, value):
        if value == '':
            return None
        return super().to_representation(value)
