import pytest
from accounts.models import Teacher

pytestmark = pytest.mark.django_db


def test_no_email_exception():
    with pytest.raises(ValueError) as er:
        Teacher.objects.create_user(name='Teacher')

    assert "User must have an email address" == str(er.value)


def test_create_account():
    Teacher.objects.create_user(name='Teacher',
                                email='teacher@test.com',
                                password='1234')

    data = Teacher.objects.first()

    assert data.name == 'Teacher'
    assert data.email == 'teacher@test.com'
    assert data.check_password('1234')
    assert data.type == 'TEACHER'
