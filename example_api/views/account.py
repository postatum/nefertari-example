from nefertari.authentication.views import (
    TokenAuthRegisterView as NefTokenAuthRegisterView,
    TokenAuthClaimView as NefTokenAuthClaimView,
    TokenAuthResetView as NefTokenAuthResetView,
)

from example_api.models import User


""" Not implemented by default nefertari ticket auth views:

    * Check for user to be active on register
    * Making user 'status' being 'active' on register
    * Checking user 'status' is not 'blocked', 'inactive' on login
    * Calling user.on_login()
"""


class TokenAuthRegisterView(NefTokenAuthRegisterView):
    Model = User


class TokenAuthClaimView(NefTokenAuthClaimView):
    Model = User


class TokenAuthResetView(NefTokenAuthResetView):
    Model = User
