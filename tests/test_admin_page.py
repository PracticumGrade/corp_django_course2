import pytest

from django.apps import apps
from django.contrib import admin


@pytest.mark.parametrize(
    'app_label, model_name, config_attrs',
    [
        (
            'courses',
            'Category',
            {
                'list_display': ('title', 'description',),
                'search_fields': ('title', 'description__contains',),
                'list_display_links': ('title',),
            },
        ),
        (
            'courses',
            'Course',
            {
                'list_display': ('title', 'author', 'category', 'is_published',),
                'list_filter': ('category', 'is_published',),
                'list_editable': ('is_published',),
                'list_display_links': ('title',),
                'readonly_fields': ('created_at', 'updated_at',),
            }
        ),
        (
            'lessons',
            'Lesson',
            {
                'list_display': ('lesson_name', 'type', 'duration',),
                'list_filter': ('type',),
                'list_display_links': ('lesson_name',),
                'list_editable': ('duration',)
            },
        ),
    ]
)
def test_admin_register(app_label, model_name, config_attrs):
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

    site = admin.site._registry[model]
    for attr, value in config_attrs.items():
        actual_value = getattr(site, attr)
        assert actual_value == value, (
            f'Убедитесь, что для модели `{model._meta.object_name}` '
            f'в админке значение атрибута `{attr}` настроено согласно заданию.'
        )
