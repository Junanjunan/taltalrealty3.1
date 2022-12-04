import jwt
from django.conf import settings
from rest_framework import authentication
from users.models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            if token is None:
                return None
            xjwt, jwt_token = token.split(" ")
            # jwt_token = token
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            pk = decoded.get('pk')
            user = User.objects.get(pk=pk)
            return (user, None)
        except ValueError:
            return None


        # username = request.META.get('HTTP_X_USERNAME')
        # if not username:
        #     return None

        # try:
        #     user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     raise exceptions.AuthenticationFailed('No such user')

        # return (user, None)