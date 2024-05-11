from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from account import viewsets
from core import exceptions, mixins, behaviors, serializer_params, actions, serializers_result
from core import models, serializers, filters


class ViewSetPermissions(ViewSet):
    permission_classes_by_action: dict = {}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class ViewSetBase(viewsets.AuthViewSetBase,
                  mixins.ExpandViewSetMixin,
                  mixins.ExportViewSetMixin,
                  mixins.HistoryViewSetMixin,
                  mixins.GroupByMixin):

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.make_queryset_expandable(request)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.make_queryset_expandable(request)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            return super(ViewSetBase, self).destroy(request, *args, **kwargs)
        except IntegrityError:
            raise exceptions.ForeignKeyException


class ReleaseNotesViewSet(ViewSetPermissions):
    permission_classes = (AllowAny,)

    @action(methods=['GET'], detail=False)
    def releases(self, request):
        behavior = behaviors.ReleaseNotesBehavior()
        result = behavior.run()

        return Response(status=status.HTTP_200_OK, data=result)


class ConfigurationViewSet(ViewSetBase):
    queryset = models.Config.objects.all()
    serializer_class = serializers.ConfigurationSerializer
    filterset_class = filters.ConfigurationFilter
    ordering_fields = '__all__'
    ordering = ('key',)


class ChurchGroupViewSet(ViewSetBase):
    queryset = models.ChurchGroup.objects.all()
    serializer_class = serializers.ChurchGroupSerializer
    filterset_class = filters.ChurchGroupFilter
    ordering_fields = '__all__'
    ordering = ('-id',)


class ChurchGroupUserViewSet(ViewSetBase):
    queryset = models.ChurchGroupUser.objects.all()
    serializer_class = serializers.ChurchGroupUserSerializer
    filterset_class = filters.ChurchGroupUserFilter
    ordering_fields = '__all__'
    ordering = ('-id',)
