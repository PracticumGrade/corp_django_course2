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
    ('is_public', BooleanField, {'default': False}),
    ('created_at', DateTimeField, {'auto_now_add': True}),
    ('updated_at', DateTimeField, {'auto_now': True}),
])
class TestCategoryModelAttrs(_TestModelAttrs):

    @property
    def model(self):
        return Course


def test__str__(mixer):
    app_label = 'courses'
    model_name = 'Course'
    title = 'Тестовое название курса'

    obj = mixer.blend(f'{app_label}.{model_name}', title=title)
    assert str(obj) == title, (
        f'Убедитесь, что в модели `{model_name}` '
        'настроено читаемое название объектов согласно заданию.'
    )


def test_author_on_delete(courses_with_author):
    author = courses_with_author[0].author
    try:
        author.delete()
    except IntegrityError:
        raise AssertionError(
            'Проверьте, что значение атрибута `on_delete` '
            'поля `author` в модели `Course` соответствует заданию.'
        )
    assert not Course.objects.filter(author=author).exists(),  (
        'Проверьте, что значение атрибута `on_delete` '
        'поля `author` в модели `Course` соответствует заданию.'
    )


def test_category_on_delete(courses_with_category):
    category = courses_with_category[0].category
    try:
        category.delete()
    except IntegrityError:
        raise AssertionError(
            'Проверьте, что значение атрибута `on_delete` '
            'поля `category` в модели `Course` соответствует заданию.'
        )
    assert not Course.objects.filter(category=category).exists(), (
        'Проверьте, что значение атрибута `on_delete` '
        'поля `category` в модели `Course` соответствует заданию.'
    )
