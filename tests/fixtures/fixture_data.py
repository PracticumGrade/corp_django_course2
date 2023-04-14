import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def author(mixer):
    User = get_user_model()
    return mixer.blend(User)
