from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_vaue(self, user, timestamp):
        # timestamp is number of seconds since 2001-1-1. Converted to base 36,
        # this gives us a 6 digit string until about 2069.
        return(
            text_type(user.pk) + text_type(timestamp)
        )

generate_token = TokenGenerator()
