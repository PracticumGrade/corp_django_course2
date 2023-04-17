import pytest


N_COURSES = 3
N_LESSONS = 10


@pytest.fixture
def courses(mixer):
    return mixer.cycle(N_COURSES).blend('courses.Course')


@pytest.fixture
def courses_with_author(mixer, author):
    return mixer.cycle(N_COURSES).blend('courses.Course', author=author)


@pytest.fixture
def lessons(mixer):
    return mixer.cycle(N_LESSONS).blend('lessons.Lesson')
