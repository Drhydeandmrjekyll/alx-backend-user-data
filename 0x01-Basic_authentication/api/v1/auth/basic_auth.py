#!/usr/bin/env python3
""" BasicAuth module for handling basic authentication """

import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """
        Extracts Base64 part Authorization header for Basic Authentication.
        """
        # Return None if authorization_header is None or not string
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None

        # Checks authorization header starts with 'Basic', contains one 'Basic'
        if (not authorization_header.startswith('Basic ') or
                authorization_header.count('Basic') != 1):
            return None

        # Get Base64 part after 'Basic '
        base64_part = authorization_header.split('Basic ')[1].strip()

        # Return Base64 part
        return base64_part
