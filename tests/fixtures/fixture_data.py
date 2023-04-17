import pytest
from django.contrib.auth import get_user_model


N_LESSONS = 10


@pytest.fixture
def author(mixer):
    User = get_user_model()
    return mixer.blend(User)


@pytest.fixture
def lessons(mixer):
    return mixer.cycle(N_LESSONS).blend('lessons.Lesson')
