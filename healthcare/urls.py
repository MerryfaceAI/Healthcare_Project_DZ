from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# Import spectacular views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Redirect root URL to Swagger UI
    path('', RedirectView.as_view(pattern_name='swagger-ui-root', permanent=False), name='root-redirect'),

    path('admin/', admin.site.urls),

    # Simple include: module + namespace
    path('patients/', include('patients.urls', namespace='patients')),

    # Schema generation (API)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI (API docs)
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    # ReDoc UI (API alternate docs)
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),

    # Root-level aliases for convenience
    path('schema/', SpectacularAPIView.as_view(), name='schema-root'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='schema-root'),
        name='swagger-ui-root'
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema-root'),
        name='redoc-root'
    ),
]
