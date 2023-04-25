import pytest

from django.apps import apps
from django.contrib import admin

from lessons.models import Lesson


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
                'list_display': ('title', 'author', 'category', 'is_public',),
                'list_filter': ('category', 'is_public',),
                'list_editable': ('is_public',),
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


def test_lesson_inline():
    try:
        from courses.admin import LessonInline
    except ImportError:
        raise AssertionError(
            f'Убедитесь, что в файле `courses/admin.py` объявлен класс `LessonInline`'
        )

    app_label = 'courses'
    model_name = 'Course'
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

    course_admin_site = admin.site._registry[model]

    assert course_admin_site.inlines == (LessonInline, ), (
        f'Убедитесь, что модель `LessonInline` настроена для отображения связанных записей'
        'в админ представлении модели `Course`.'
    )


@pytest.mark.parametrize(
    'expected_inline_class, config_attrs',
    [
        (admin.StackedInline, {'model': Lesson, 'extra': 0}),
    ]
)
def test_lesson_inline_config(expected_inline_class, config_attrs):
    try:
        from courses.admin import LessonInline
    except ImportError:
        raise AssertionError(
            f'Убедитесь, что в файле `courses/admin.py` объявлен класс `LessonInline`'
        )

    assert issubclass(LessonInline, expected_inline_class), (
        f'Убедитесь, что в файле `courses/admin.py` класс `LessonInline` унаследован согласно заданию.'
    )

    for attr, value in config_attrs.items():
        actual_value = getattr(LessonInline, attr)
        assert actual_value == value, (
            f'Убедитесь, что в файле `courses/admin.py` для класса `LessonInline` '
            f'значение атрибута `{attr}` настроено согласно заданию.'
        )
