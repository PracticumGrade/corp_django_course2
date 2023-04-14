import pytest

from django.apps import apps
from django.contrib import admin


@pytest.mark.parametrize(
    'app_label, model_name',
    [
        ('courses', 'Category'),
        ('courses', 'Course'),
        ('lessons', 'Lesson'),
    ]
)
def test_admin_register(app_label, model_name):
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        raise AssertionError(
            f'Убедитесь, что модель `{model_name}` объявлена в приложении `{app_label}`'
        )
    assert model in admin.site._registry, (
        f'Убедитесь, что модель `{model._meta.object_name}` '
        'зарегистрирована в админке.'
    )
