import dataclasses
from flask import Blueprint, request
from src.models.user import SubscriptionStatus
from src.repository.firestore.firestore_db import firestore_db
from src.service import authentication

USERS = Blueprint('user', __name__, url_prefix='/user')


@USERS.route("/")
def hello():
    """Greetings endpoint."""
    return "Hello auth"


@USERS.route('/tokenSign', methods=['POST'])
def check_subscription():
    """Check subscription status for the provider"""
    auth_info = request.get_json()
    provider = authentication.provider(auth_info.get('provider'))
    if provider is None:
        # Return 405 - Method Not Allowed
        return ""
    user = provider.sign_token(auth_info.get('token'))
    if user is None:
        # Return 401 - Unauthorized
        return ""
    current_user_state = firestore_db() \
        .users() \
        .get_by_id(user.user_id)
    if current_user_state is None:
        user.subscription = SubscriptionStatus.INACTIVE.value
        firestore_db() \
            .users() \
            .insert(user)
        current_user_state = user
        # Welcome new user!
    return dataclasses.asdict(current_user_state)
