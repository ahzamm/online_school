import pytest
from accounts.models import Admin

pytestmark = pytest.mark.django_db


def test_no_email_exception():
    with pytest.raises(ValueError) as er:
        Admin.objects.create_user(name="Admin")  # act
        assert "User must have an email address" == str(er.value)


def test_create_account():

    Admin.objects.create_user(  # act
        name="Admin",
        email="admin@test.com",
        password="1234",
    )

    # assert
    data = Admin.objects.first()
    assert data.name == "Admin"
    assert data.email == "admin@test.com"
    assert data.check_password("1234")
    assert data.type == "ADMIN"
