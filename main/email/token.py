from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return super()._make_hash_value(user, timestamp)

activation_token = TokenGenerator()
