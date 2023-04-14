import pytest
from django.db.models import (
    CharField, DateTimeField, ForeignKey, TextField, PositiveSmallIntegerField, TextChoices
)
from django.db.utils import IntegrityError

from lessons.models import Lesson
from tests.conftest import _TestModelAttrs

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(
    'attr, value, label',
    [
        ('EDU', 'edu', 'Программирование'),
        ('THEORY', 'theory', 'Теория'),
        ('QUIZ', 'quiz', 'Викторина'),
    ]
)
def test_exists_lesson_type_inner_class(attr, value, label):
    assert hasattr(Lesson, 'LessonType'), (
        'Проверьте, что в файле `lessons/models.py` '
        'в модели `Lesson` объявлен класс `LessonType`.'
    )

    actual_attr = getattr(Lesson.LessonType, attr, None)
    assert actual_attr is not None and actual_attr.value == value and actual_attr.label == label, (
        'Проверьте, что в файле `lessons/models.py` '
        f'в модели `Lesson` в классе `LessonType` атрибут `{attr}` соответствует заданию.'
    )


@pytest.mark.parametrize(('field', 'type', 'params'), [
    ('title', CharField, {'max_length': 256}),
    ('text', TextField, {}),
    ('type', CharField, {'max_length': 16, 'choices': [('edu', 'Программирование'), ('theory', 'Теория'), ('quiz', 'Викторина')]}),
    ('duration', PositiveSmallIntegerField, {}),
    ('course', ForeignKey, {'null': False}),
    ('created_at', DateTimeField, {'auto_now_add': True}),
    ('updated_at', DateTimeField, {'auto_now': True}),
])
class TestCategoryModelAttrs(_TestModelAttrs):

    @property
    def model(self):
        return Lesson


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
    assert not Lesson.objects.filter(author=author).exists(),  (
        'Проверьте, что значение атрибута `on_delete` '
        'поля `author` в модели `Post` соответствует заданию.'
    )
