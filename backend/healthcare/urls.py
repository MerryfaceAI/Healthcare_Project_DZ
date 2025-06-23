# backend/healthcare/urls.py

from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from patients.api_views import CSRFExemptObtainAuthToken

urlpatterns = [
    # 1) Admin site
    path('admin/', admin.site.urls),

    # 2) Django's built-in auth (login/logout/password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # 3) Token-auth endpoint (uses our CSRFExemptObtainAuthToken view)
    path(
        'api/token-auth/',
        CSRFExemptObtainAuthToken.as_view(),
        name='api_token_auth'
    ),

    # 4) All DRF viewsets & custom endpoints for the "patients" app
    path(
        'api/',
        include(('patients.urls.api', 'patients_api'), namespace='patients_api')
    ),

    # 5) DRF's session-based login/logout for the browsable API
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),

    # 6) OpenAPI schema (JSON) and interactive Swagger UI
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='api-schema'
    ),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-swagger-ui'
    ),

    # 7) Optional server-rendered HTML views for patients
    path(
        'patients/',
        include(('patients.urls.html', 'patients_html'), namespace='patients_html')
    ),
]
