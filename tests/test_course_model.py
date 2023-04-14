import pytest
from django.db.models import (
    BooleanField, CharField, DateTimeField, ForeignKey, TextField)
from django.db.utils import IntegrityError

from courses.models import Course
from tests.conftest import _TestModelAttrs

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(('field', 'type', 'params'), [
    ('title', CharField, {'max_length': 256}),
    ('description', TextField, {}),
    ('author', ForeignKey, {'null': False}),
    ('category', ForeignKey, {'null': False}),
    ('is_published', BooleanField, {'default': False}),
    ('created_at', DateTimeField, {'auto_now_add': True}),
    ('updated_at', DateTimeField, {'auto_now': True}),
])
class TestCategoryModelAttrs(_TestModelAttrs):

    @property
    def model(self):
        return Course


@pytest.mark.skip(reason='Пока не реализовано')  # FIXME адаптировать под Course
def test_author_on_delete(posts_with_author):
    author = posts_with_author[0].author
    try:
        author.delete()
    except IntegrityError:
        raise AssertionError(
            'Проверьте, что значение атрибута `on_delete` '
            'поля `author` в модели `Post` соответствует заданию.'
        )
    assert not Course.objects.filter(author=author).exists(),  (
        'Проверьте, что значение атрибута `on_delete` '
        'поля `author` в модели `Post` соответствует заданию.'
    )


@pytest.mark.skip(reason='Пока не реализовано')  # FIXME адаптировать под Course
def test_location_on_delete(posts_with_published_locations):
    location = posts_with_published_locations[0].location
    try:
        location.delete()
    except IntegrityError:
        raise AssertionError(
            'Проверьте, что значение атрибута `on_delete` '
            'поля `location` в модели `Post` соответствует заданию.'
        )
    assert Course.objects.filter(location=location).exists(), (
        'Проверьте, что значение атрибута `on_delete` '
        'поля `location` в модели `Post` соответствует заданию.'
    )
