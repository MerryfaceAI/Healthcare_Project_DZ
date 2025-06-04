# patients/api_views.py

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    This class disables CSRF enforcement on session‐authenticated requests.
    We’ll use it if we ever want SessionAuth without requiring a CSRF token.
    """
    def enforce_csrf(self, request):
        return  # simply do not enforce CSRF


class CSRFExemptObtainAuthToken(ObtainAuthToken):
    """
    Identical to DRF’s ObtainAuthToken, but we remove SessionAuthentication
    and BasicAuthentication, and allow any user (so we can wrap it in csrf_exempt).
    """
    authentication_classes = ()            # no session/basic auth here
    permission_classes = (AllowAny,)       # anyone can attempt to get a token

    def post(self, request, *args, **kwargs):
        # Simply delegate to ObtainAuthToken; since we're wrapping this view in csrf_exempt,
        # no CSRF check is done.
        return super().post(request, *args, **kwargs)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "groups": [{"name": g.name} for g in user.groups.all()],
    })