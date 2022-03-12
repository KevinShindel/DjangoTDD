from accounts.models import User, Token


class PasswordlessAuthenticationBackend:

    @staticmethod
    def authenticate(uid):
        try:
            token = Token.objects.get(uid=uid)
        except Token.DoesNotExist:
            return None
        user, exist = User.objects.get_or_create(email=token.email)
        return user

    @staticmethod
    def get_user(email):
        return User.objects.get(email=email)
