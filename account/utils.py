from account import serializers


def get_user(user, request=None):
    from account.serializers import UserAuthSerializer
    serializer = UserAuthSerializer(user, context={'request': request})
    return serializer.data


def get_user_login(user, request=None):
    from account.serializers import UserLoginSerializer
    serializer = UserLoginSerializer(user, context={'request': request})
    return serializer.data


def get_custom_jwt(user):
    token = serializers.MyTokenObtainPairSerializer().get_token(user)
    return token


def get_custom_token_query(refresh):
    """Create url query with refresh and access token"""
    return "?%s%s%s%s%s" % ("refresh=", str(refresh), "&", "access=", str(refresh.access_token))


def create_user(user):
    from account import models

    target_user = models.User.objects.get(username=user['email'])
    target_user.email = user['email']
    target_user.name = f"{user['user_identity']['first_name'][0]} {user['user_identity']['last_name'][0]}"
    target_user.save()
