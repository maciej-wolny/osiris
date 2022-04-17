# pylint: disable=C0103
# pylint: disable=R0903
# rules irrelevant for this design
from google.oauth2 import id_token
from google.auth.transport import requests

from src.models.user import User
from src.models.user import Provider

SUPPORTED_ISS = ['accounts.google.com', 'https://accounts.google.com']
CLIENT_ID = "580560711588-j2oalj996ncpdor4ap3afba0pificq22.apps.googleusercontent.com"


def provider(provider_type):
    """Get provider object that provides sign_token function"""
    return AUTH_MAPPING.get(provider_type, None)


class GoogleAuth:
    @staticmethod
    def sign_token(token):
        """Google implementation of sign token. Details can be found here:
        https://developers.google.com/identity/sign-in/web/backend-auth """
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            if idinfo['iss'] not in SUPPORTED_ISS:
                raise ValueError('Wrong issuer.')
            return User(provider=Provider.GOOGLE.value,
                        subscription="",
                        mail=idinfo.get('email'),
                        name=idinfo.get('given_name'),
                        surname=idinfo.get('family_name'),
                        user_id=idinfo.get('sub'),
                        picture=idinfo.get('picture'),
                        token=token)
        except ValueError:
            return None


class FacebookAuth:
    @staticmethod
    def sign_token(token):
        """TO BE DONE"""


class MicrosoftAuth:
    @staticmethod
    def sign_token(token):
        """TO BE DONE"""


AUTH_MAPPING = {
    Provider.GOOGLE.name: GoogleAuth,
    Provider.FACEBOOK.name: FacebookAuth,
    Provider.MICROSOFT.name: MicrosoftAuth,
}
