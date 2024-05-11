import jwt
from django.http import JsonResponse

from account.models import LoggedInUser


class JWTTokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_AUTHORIZATION" in request.META:
            token = request.META["HTTP_AUTHORIZATION"].replace("Bearer ", "")
            if token is not None and token != "null" and not token.startswith("Basic"):
                decoded = jwt.decode(token, options={"verify_signature": False})
                logged_user = LoggedInUser.objects.filter(user=decoded["user_id"]).order_by("-created_at")
                if logged_user.exists() and logged_user.first().last_token != token:
                    return JsonResponse({"message": "User logged in on another terminal."}, status=401)

        return self.get_response(request)
