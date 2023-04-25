import pytest
from django.urls import reverse

from lessons.admin import LessonAdmin


pytestmark = [
    pytest.mark.django_db,
]


def test_view(admin_client, django_assert_num_queries, lessons):
    url = reverse('admin:lessons_lesson_changelist')
    try:
        with django_assert_num_queries(5):
            admin_client.get(url)
    except pytest.fail.Exception as e:
        raise AssertionError(
            'Убедитесь, что при выводе множества уроков в админке `LessonAdmin` '
            'используется оптимизация запросов согласно заданию.'
        ) from e

    assert getattr(LessonAdmin, 'list_select_related') == ('course', ), (
        'Убедитесь, что оптимизация запроса множества уроков в админке `LessonAdmin` '
        'выполнена согласно заданию.'
    )


def test_lesson_name(admin_client, lessons):
    assert hasattr(LessonAdmin, 'lesson_name'), (
        'Проверьте, что в админке `LessonAdmin` объявлен метод `lesson_name` согласно заданию.'
    )
    assert getattr(LessonAdmin.lesson_name, 'short_description', None) == 'Название урока', (
        'Проверьте, что в админке `LessonAdmin` для метода `lesson_name` '
        'задан атрибут `short_description` согласно заданию.'
    )

    url = reverse('admin:lessons_lesson_changelist')
    response = admin_client.get(url)
    list_lesson_names = [
        f'{lesson.course}: {lesson}' for lesson in lessons
    ]
    content = response.content.decode('utf-8')
    for lesson_name in list_lesson_names:
        assert lesson_name in content, (
            'Убедитесь, что в админке `LessonAdmin` метод `lesson_name` '
            'возвращает значение согласно заданию.'
        )
