from app.models import User
from app.core.config import settings
from app.core.security import get_password_hash

import factory


class UserFactory(factory.Factory):
    """User factory."""
    username = settings.FIRST_USER_USERNAME
    hashed_password = get_password_hash(
        settings.FIRST_USER_PASSWORD.get_secret_value()
    )

    def __init__(self, username, hashed_password):
        username = username
        hashed_password = get_password_hash(
          hashed_password
        )

    class Meta:
        """Factory configuration."""
        model = User
