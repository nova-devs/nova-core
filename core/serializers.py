from django.db import models as dj_models, transaction
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from account import models as account_models
from core import fields as core_fields, models


class SerializerBase(FlexFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    serializer_field_mapping = {
        dj_models.AutoField: serializers.IntegerField,
        dj_models.BigIntegerField: serializers.IntegerField,
        dj_models.BooleanField: serializers.BooleanField,
        dj_models.CharField: serializers.CharField,
        dj_models.CommaSeparatedIntegerField: serializers.CharField,
        dj_models.DateField: serializers.DateField,
        dj_models.DateTimeField: core_fields.DateTimeFieldWithTZ,
        dj_models.DecimalField: serializers.DecimalField,
        dj_models.EmailField: serializers.EmailField,
        dj_models.Field: serializers.ModelField,
        dj_models.FileField: serializers.FileField,
        dj_models.FloatField: serializers.FloatField,
        dj_models.ImageField: serializers.ImageField,
        dj_models.IntegerField: serializers.IntegerField,
        dj_models.PositiveIntegerField: serializers.IntegerField,
        dj_models.PositiveSmallIntegerField: serializers.IntegerField,
        dj_models.SlugField: serializers.SlugField,
        dj_models.SmallIntegerField: serializers.IntegerField,
        dj_models.TextField: serializers.CharField,
        dj_models.TimeField: serializers.TimeField,
        dj_models.URLField: serializers.URLField,
        dj_models.GenericIPAddressField: serializers.IPAddressField,
        dj_models.FilePathField: serializers.FilePathField,
    }

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.insert(0, 'id')
        return fields


class UserHistorySerializer(SerializerBase):
    class Meta:
        model = account_models.User
        fields = ['id', 'url', 'name']


class HistoryListSerializer(serializers.Serializer):
    history_date = serializers.DateTimeField(required=True)
    history_user = UserHistorySerializer()
    history_type = serializers.CharField(required=True, max_length=10)
    changes = serializers.ListSerializer(
        child=serializers.JSONField()
    )


class UserHyperlinkedModelSerializer(SerializerBase):
    class Meta:
        model = account_models.User
        fields = ['url', 'username', 'name']


class ConfigurationSerializer(SerializerBase):
    class Meta:
        model = models.Config
        fields = '__all__'


class ChurchGroupSerializer(SerializerBase):
    class Meta:
        model = models.ChurchGroup
        fields = "__all__"


class ChurchGroupUserSerializer(SerializerBase):
    expandable_fields = {
        'user': (
            'account.UserSerializer',
            {'fields': ['name']}
        )
    }

    class Meta:
        model = models.ChurchGroupUser
        fields = "__all__"
