import importlib

import pytest
from django.apps import apps
from django.conf import settings


def test_rus_localization():
    assert hasattr(settings, 'LANGUAGE_CODE'), (
        'В настройках приложения не обнаружен ключ `LANGUAGE_CODE`.'
    )
    assert settings.LANGUAGE_CODE == 'ru-RU', (
        'В настройках приложения значение ключа '
        '`LANGUAGE_CODE` должно быть `ru-RU`.'
    )


@pytest.mark.parametrize(
    'app_label, verbose_name',
    [
        ('courses', 'Курс'),
        ('lessons', 'Урок'),
    ]
)
def test_app_verbose_name(app_label, verbose_name):
    try:
        application = apps.get_app_config(app_label)
    except LookupError:
        raise AssertionError(
            f'Убедитесь, что зарегистрировано приложение `{app_label}`'
        )
    assert application.verbose_name == verbose_name, (
        f'Приложение `{app_label.capitalize()}` не локализированно.'
    )


@pytest.mark.parametrize(('n_app', 'n_model', 'n_verbose', 'n_verbose_plural'), [
    ('courses', 'Category', 'категория', 'Категории'),
    ('courses', 'Course', 'курс', 'Курсы'),
    ('lessons', 'Lesson', 'урок', 'Уроки'),
])
def test_models_translated(n_app, n_model, n_verbose, n_verbose_plural):
    module = importlib.import_module(f'{n_app}.models')
    model = getattr(module, n_model)
    assert model._meta.verbose_name == n_verbose, (
        f'Убедитесь, что в приложении `{n_app}` в модели `{n_model}` во вложенном классе `Meta` значение для '
        f'`verbose_name` установлено в соответствии с заданием.'
    )
    assert (
        model._meta.verbose_name_plural == n_verbose_plural
    ), (
        f'Убедитесь, что в приложении `{n_app}` в модели `{n_model}` во вложенном классе `Meta` значение для '
        '`verbose_name_plural` установлено в соответствии с заданием.'
    )


@pytest.mark.parametrize(('n_app', 'n_model', 'param', 'n_verbose'), [
    ('courses', 'Category', 'title', 'Заголовок'),
    ('courses', 'Category', 'description', 'Описание'),
    ('courses', 'Category', 'slug', 'Идентификатор'),
    ('courses', 'Category', 'created_at', 'Добавлено'),
    ('courses', 'Course', 'title', 'Заголовок'),
    ('courses', 'Course', 'description', 'Описание'),
    ('courses', 'Course', 'author', 'Автор курса'),
    ('courses', 'Course', 'category', 'Категория'),
    ('courses', 'Course', 'is_public', 'Публичный'),
    ('courses', 'Course', 'created_at', 'Добавлено'),
    ('courses', 'Course', 'updated_at', 'Отредактировано'),
    ('lessons', 'Lesson', 'title', 'Заголовок'),
    ('lessons', 'Lesson', 'text', 'Текст'),
    ('lessons', 'Lesson', 'type', 'Тип урока'),
    ('lessons', 'Lesson', 'duration', 'Продолжительность'),
    ('lessons', 'Lesson', 'course', 'Курс'),
    ('lessons', 'Lesson', 'created_at', 'Добавлено'),
    ('lessons', 'Lesson', 'updated_at', 'Отредактировано'),
])
def test_models_params_translate(n_app, n_model, param, n_verbose):
    module = importlib.import_module(f'{n_app}.models')
    model = getattr(module, n_model)
    field = model._meta.get_field(param)
    assert field.verbose_name == n_verbose, (
        f'Убедитесь, что в приложении `{n_app}` в модели `{n_model}` значение `verbose_name` '
        f' для атрибута `{param}` '
        'установлено в соответствии с заданием.'
    )


@pytest.mark.parametrize(('n_app', 'n_model', 'param', 'text'), [
    (
        'courses',
        'Course',
        'is_public',
        'Установите галочку, чтобы сделать курс публичным.'
    ),
    (
        'courses',
        'Category',
        'slug',
        'Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    ),
    (
        'lessons',
        'Lesson',
        'duration',
        'Укажите продолжительность курса в минутах.'
    )
])
def test_help_text_translate(n_app, n_model, param, text):
    module = importlib.import_module(f'{n_app}.models')
    model = getattr(module, n_model)
    field = model._meta.get_field(param)
    assert field.help_text == text, (
        f'Убедитесь, что в приложении `{n_app}` в модели `{n_model}` значение `help_text` '
        f'для атрибута `{param}` '
        'установлено в соответствии с заданием.'
    )
