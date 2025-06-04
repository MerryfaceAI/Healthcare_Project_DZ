# healthcare/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Import our custom token‐view from patients/api_views.py
from patients.api_views import CSRFExemptObtainAuthToken

urlpatterns = [
    # 1) Django admin
    path('admin/', admin.site.urls),

    # 2) Built‐in Django auth (login/logout/password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # 3) Our CSRF‐exempt token endpoint
    path(
        'api/token-auth/',
        csrf_exempt(CSRFExemptObtainAuthToken.as_view()),
        name='api-token-auth'
    ),

    # 4) All of the “patients” API endpoints (ViewSets + custom FVs)
    path(
        'api/',
        include(('patients.urls.api', 'patients-api'), namespace='patients-api')
    ),

    # 5) DRF browsable‐API login/logout (optional)
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),

    # 6) Swagger/OpenAPI schema & docs
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-swagger-ui'),

    # 7) If you still serve server‐rendered HTML “patients” pages, keep them here:
    path(
        'patients/',
        include(('patients.urls.html', 'patients_html'), namespace='patients_html')
    ),
    
    # 8) (Optional) Home redirect—replace 'patients_html:patient_list' with whatever makes sense:
    # path('', RedirectView.as_view(pattern_name='patients_html:patient_list', permanent=False), name='home'),
]
