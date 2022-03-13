from accounts.models import User, Token


class PasswordlessAuthenticationBackend:

    @staticmethod
    def authenticate(uid):
        try:
            token = Token.objects.get(uid=uid)
            user, created = User.objects.get_or_create(email=token.email)
            return user
        except Token.DoesNotExist:
            return None

    @staticmethod
    def get_user(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
