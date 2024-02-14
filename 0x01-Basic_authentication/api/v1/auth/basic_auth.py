#!/usr/bin/env python3
""" BasicAuth module for handling basic authentication """

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class """

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Method to extract user email and password """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None

        decoded_credentials = base64.b64decode(
            decoded_base64_authorization_header.encode('utf-8')
        ).decode('utf-8')

        # Split decoded credentials into email and password
        credentials = decoded_credentials.split(':', 1)
        if len(credentials) != 2:
            return None, None

        user_email, user_password = credentials
        return user_email, user_password

    def user_object_from_credentials(
            self,
            user_email: str, user_password: str
    ) -> TypeVar('User'):
        """ Returns User instance based on email and password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_password is None or not isinstance(user_password, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_password):
                return user

        return None

    def current_user(
            self,
            request=None
    ) -> TypeVar('User'):
        """ Retrieve User instance for a request """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
                auth_header)
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)
        if decoded_auth_header is None:
            return None

        user_email, user_password = self.extract_user_credentials(
                decoded_auth_header)
        if user_email is None or user_password is None:
            return None

        user = self.user_object_from_credentials(user_email, user_password)
        return user
