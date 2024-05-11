from django_filters import filterset

from core import models

LIKE = 'unaccent__icontains'
EQUALS = 'exact'
IN = 'in'
LT = 'lt'
GT = 'gt'
LTE = 'lte'
GTE = 'gte'


class ConfigurationFilter(filterset.FilterSet):
    key = filterset.CharFilter(lookup_expr=LIKE)
    value = filterset.CharFilter(lookup_expr=LIKE)

    class Meta:
        model = models.Config
        fields = ['key', 'value']


class ChurchGroupFilter(filterset.FilterSet):
    description = filterset.CharFilter(lookup_expr=LIKE)
    type = filterset.CharFilter(lookup_expr=EQUALS)
    category = filterset.CharFilter(lookup_expr=EQUALS)

    class Meta:
        model = models.ChurchGroup
        fields = ['is_active',
                  'description', 'type', 'category']


class ChurchGroupUserFilter(filterset.FilterSet):
    church_group_id = filterset.NumberFilter(lookup_expr=EQUALS, field_name='church_group_id')
    user_id = filterset.NumberFilter(lookup_expr=EQUALS, field_name='user_id')
    association_type = filterset.CharFilter(lookup_expr=EQUALS)

    class Meta:
        model = models.ChurchGroupUser
        fields = ['church_group_id', 'user_id', 'association_type']
