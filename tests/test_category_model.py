import pytest
from django.db.models import (
    CharField,
    SlugField,
    TextField,
    DateTimeField
)

from courses.models import Category
from tests.conftest import _TestModelAttrs

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(('field', 'type', 'params'), [
    ('title', CharField, {'max_length': 256}),
    ('description', TextField, {}),
    ('slug', SlugField, {'_unique': True}),
    ('created_at', DateTimeField, {'auto_now_add': True}),
])
class TestCategoryModelAttrs(_TestModelAttrs):

    def get_parameter_display_name(self, param):
        return 'unique' if param == '_unique' else param

    @property
    def model(self):
        return Category


def test__str__(mixer):
    app_label = 'courses'
    model_name = 'Category'
    title = 'Тестовое название категории'
    obj = mixer.blend(f'{app_label}.{model_name}', title=title)

    assert str(obj) == title, (
        f'Убедитесь, что в модели `{model_name}` '
        'настроено читаемое название объектов согласно заданию.'
    )
