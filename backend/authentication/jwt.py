from sys import prefix
from coreapi import auth
from django.conf import settings
import jwt
from rest_framework import authentication, exceptions
from django.contrib.auth.models import User


# sets up an authentication schema
class JWTAuthentication(authentication.BaseAuthentication):
    # override the built in method authenticate so that we can check whether we should authenticate this user or not
    def authenticate(self, request):

        # gets the header where the user would be sending the token
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:  # checks whether the user is supplying auth data and returns none if it is not
            return None
        # decodes the data from a byte format to a format python can read
        # This converts the data that is coming from a network in the byte format to a string format readable by python.
        prefix, token = auth_data.decode('utf-8').split(' ')
        # Splitting by space makes sure the prefix would be in the first index and the corresponding token would be in the second index

        # validating the token
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms="HS256")  # gets the jwt payload and decodes the token the user provides and  the token signature

            # adds the username to the payload after it has been decoded
            user = User.objects.get(username=payload["username"])
            return (user, token)

        except jwt.DecodeError as identifier:  # throws an error if the token is invalid or has been tampered with
            raise exceptions.AuthenticationFailed(
                'Your token is invalid, login')

        except jwt.ExpiredSignatureError as identifier:  # throws an error if the token has expired
            raise exceptions.AuthenticationFailed(
                'Your token has expired')

        return super().authenticate(request)
