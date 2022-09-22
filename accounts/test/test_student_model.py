import pytest
from accounts.models import Student

pytestmark = pytest.mark.django_db


def test_no_email_exception():
    with pytest.raises(ValueError) as er:
        Student.objects.create_user(name='Student')

    assert "User must have an email address" == str(er.value)


def test_create_account():
    Student.objects.create_user(
        name='Student', email='student@test.com', password='1234')
    data = Student.objects.first()

    assert data.name == 'Student'
    assert data.email == 'student@test.com'
    assert data.check_password('1234')
    assert data.type == 'STUDENT'
