import pytest


N_COURSES = 3
N_LESSONS = 10


@pytest.fixture
def category(mixer):
    return mixer.blend('courses.Category')


@pytest.fixture
def course(mixer):
    return mixer.blend('courses.Course')


@pytest.fixture
def courses(mixer):
    return mixer.cycle(N_COURSES).blend('courses.Course')


@pytest.fixture
def courses_with_author(mixer, author):
    return mixer.cycle(N_COURSES).blend('courses.Course', author=author)


@pytest.fixture
def courses_with_category(mixer, category):
    return mixer.cycle(N_COURSES).blend('courses.Course', category=category)


@pytest.fixture
def lessons(mixer):
    return mixer.cycle(N_LESSONS).blend('lessons.Lesson')


@pytest.fixture
def lessons_with_course(mixer, course):
    return mixer.cycle(N_LESSONS).blend('lessons.Lesson', course=course)
