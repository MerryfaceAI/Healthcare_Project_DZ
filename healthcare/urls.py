# healthcare/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # 1) Root → patient list
    path(
        '',
        RedirectView.as_view(pattern_name='patients:patient_list', permanent=False),
        name='root-redirect'
    ),

    # 2) Admin
    path('admin/', admin.site.urls),

    # 3) Django auth
    path('accounts/', include('django.contrib.auth.urls')),

    # 4) Main site (HTML views)
    path(
        'patients/',
        include(('patients.urls.html', 'patients'), namespace='patients')
    ),

    # 5) API (JSON + docs + token auth)
    #    Note: include the correct app_name ('api') to match patients/urls/api.py
    path(
        'api/',
        include(('patients.urls.api', 'api'), namespace='api')
    ),
    # secondary API mount under /patients/api/ for backwards-compatibility
    path(
        'patients/api/',
        include(('patients.urls.api', 'api'), namespace='patients-api')
    ),
    path('api-auth/', include('rest_framework.urls')),             # browsable login
    path('api/token-auth/', obtain_auth_token, name='token-auth'), # token endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
