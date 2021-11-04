from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from backend.constants import SWAGGER_URL_PREFIX

urlpatterns = [
    path('admin/', admin.site.urls),

    # Open API documentation
    path(f'{SWAGGER_URL_PREFIX}/api/', SpectacularAPIView.as_view(), name='schema'),
    path(f'{SWAGGER_URL_PREFIX}/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f'{SWAGGER_URL_PREFIX}/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API
    path('', include('tasks.urls')),
    path('', include('tournaments.urls')),
]
