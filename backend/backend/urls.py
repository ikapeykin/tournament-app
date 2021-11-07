from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Face App Challenge API",
        default_version='v1',
        description="OpenAPI",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Open API documentation
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # API
    path('', include('tasks.urls')),
    path('', include('tournaments.urls')),
]
