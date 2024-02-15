#!/usr/bin/env python3
"""
Module for handling SessionDBAuth authentication routes
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class for database session-based authentication """
    def create_session(self, user_id=None):
        """ Create session ID and store in database """
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return User ID based on Session ID """
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroy session ID stored in database """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False
        user_session[0].remove()
        return True
