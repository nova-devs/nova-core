from rest_framework.routers import DefaultRouter

from core import viewsets

router = DefaultRouter()
router.register('release_notes', viewsets.ReleaseNotesViewSet, basename='release_notes')
router.register("config", viewsets.ConfigurationViewSet)
router.register('church_group', viewsets.ChurchGroupViewSet)
router.register('church_group_user', viewsets.ChurchGroupUserViewSet)
urlpatterns = router.urls
