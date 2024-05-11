from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, reverse, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from nova import settings

urlpatterns = [
    path('', lambda request: redirect(reverse('api-root'))),
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls'), name='api-root'),
    path('api/account/', include('account.urls')),
]

PATHS_TO_ADD = ['^api/account/', '^api/nova/']
api_urls = [item for item in urlpatterns if
            hasattr(item, 'pattern') and item.pattern.regex.pattern in PATHS_TO_ADD]

schema_view = get_schema_view(
    openapi.Info(
        title="nova-core API",
        default_version='v1',
        description="Documentation: This model is used to describe existing endpoints in nova Project.",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=api_urls
)

urlpatterns += [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns.append(path('rosetta/', include('rosetta.urls')))
