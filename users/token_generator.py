from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

"""
function to generate account generation token
"""


class AccountTokenGenerator(PasswordResetTokenGenerator):
    def make_hash_values(self, user, timestamp):
        token = text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)

        return token


activation_token = AccountTokenGenerator()
