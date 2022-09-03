from django.urls import reverse
import json
import mailbox
from email import message
from unittest.mock import patch
import pytest
from django.core import mail
from django.test import Client, TestCase

pytestmark = pytest.mark.django_db


def test_ending_emails(mailoutbox):
    assert len(mailoutbox) == 0

    mail.send_mail(subject='TestSubject', message='TestMessage',
                   from_email='test@gmail.com', recipient_list=['test1@gmail.com'], fail_silently=False)

    m = mailoutbox[0]
    assert m.subject == 'TestSubject'
    assert m.body == 'TestMessage'
    assert m.from_email == 'test@gmail.com'
    assert list(m.to) == ['test1@gmail.com']

    assert len(mailoutbox) == 1


def test_reset_password_with_wrong_email(client):
    response = client.post(reverse("Admin_Reset_Password"), data={
                           "email": "ahzamahmed6@gmail.com"})
    response_content = json.loads(response.content)
    error_message = {
        "errors": {
            "non_field_errors": [
                "User with this email doesnot exist"
            ]
        }
    }
    assert response_content == error_message


@pytest.fixture
def create_test_student_with_legit_email(client, create_test_admin):
    data = {
        "email": "ahzamahmed6@gmail.com",
        "name": "Student",
        "password": "1234",
        "password2": "1234"
    }
    token = create_test_admin
    response = client.post(reverse("Student_Register"),
                           data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    return response_content['token']['access']


def test_reset_password_response(client, create_test_student_with_legit_email):
    response = client.post(reverse("Admin_Reset_Password"), data={
                           "email": "ahzamahmed6@gmail.com"})
    response_content = json.loads(response.content)

    assert response_content == {
        "msg": "Email sent successfully"
    }


@patch("accounts.serializers.PasswordResetTokenGenerator.make_token")
@patch("accounts.serializers.urlsafe_base64_encode")
def test_reset_password_mail(patch_encode, make_token, client, create_test_student_with_legit_email, mailoutbox):
    patch_encode.return_value = "thisispatchencode"
    make_token.return_value = "thisispatchtoken"
    response = client.post(reverse("Admin_Reset_Password"), data={
                           "email": "ahzamahmed6@gmail.com"})
    reset_link = "http://localhost:8000/api/account/reset/thisispatchencode/thisispatchtoken"
    mail_message = mailoutbox[0]
    assert mail_message.body.split(' ')[-1] == reset_link


@patch('accounts.views.get_tokens_for_user')
def test_reset_password(patch_token, client, create_test_student_with_legit_email, student_login, mailoutbox):
    response = client.post(reverse("Admin_Reset_Password"), data={
        "email": "ahzamahmed6@gmail.com"})
    mail_message = mailoutbox[0]
    reset_link = mail_message.body.split(' ')[-1] + '/'
    data = {"password": "changed_password", "password2": "changed_password"}
    response = client.post(reset_link, data=data)
    response_content = json.loads(response.content)
    assert response_content == {'msg': 'Password Reset Successfully'}

    response = student_login(patch_token=patch_token, client=client,
                             email="ahzamahmed6@gmail.com", password="changed_password")

    response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content == {
        "msg": "Login Success",
        "token": {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken"
        }
    }
