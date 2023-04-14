import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer as _mixer

try:
    from courses.models import Category, Course  # noqa:F401
    from lessons.models import Lesson  # noqa:F401
except ImportError as e:
    models = {
        'courses': ['Category', 'Course'],
        'lessons': ['Lesson']
    }
    raise AssertionError(
        f'В приложении `{e.name}` опишите '
        f'модели `{", ".join(models[e.name])}`'
    )
except RuntimeError:
    registered_apps = set(app.name for app in apps.get_app_configs())
    need_apps = {'courses': 'courses', 'lessons': 'lessons'}
    if not set(need_apps.values()).intersection(registered_apps):
        need_apps = {
            'courses': 'courses.apps.CoursesConfig', 'lessons': 'lessons.apps.LessonsConfig'}

    for need_app_name, need_app_conf_name in need_apps.items():
        if need_app_conf_name not in registered_apps:
            raise AssertionError(
                f'Убедитесь, что зарегистрировано приложение {need_app_name}'
            )

pytest_plugins = [
    'fixtures.fixture_data'
]


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user(mixer):
    User = get_user_model()
    return mixer.blend(User)


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


class _TestModelAttrs:

    @property
    def model(self):
        raise NotImplementedError(
            'Override this property in inherited test class')

    def get_parameter_display_name(self, param):
        return param

    def test_model_attrs(self, field, type, params):
        model_name = self.model.__name__
        assert hasattr(self.model, field), (
            f'В модели `{model_name}` укажите атрибут `{field}`.')
        model_field = self.model._meta.get_field(field)
        assert isinstance(model_field, type), (
            f'В модели `{model_name}` у атрибута `{field}` '
            f'укажите тип `{type}`.'
        )
        for param, value_param in params.items():
            display_name = self.get_parameter_display_name(param)
            assert param in model_field.__dict__, (
                f'В модели `{model_name}` для атрибута `{field}` '
                f'укажите параметр `{display_name}`.'
            )
            assert model_field.__dict__.get(param) == value_param, (
                f'В модели `{model_name}` в атрибуте `{field}` '
                f'проверьте значение параметра `{display_name}` '
                'на соответствие заданию.'
            )
