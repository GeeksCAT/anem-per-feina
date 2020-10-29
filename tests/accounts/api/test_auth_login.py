import json

import jwt
import pytest
from rest_framework import status

from tests.conftest import CONTENT_TYPE_JSON, EMAIL, PASSWORD

DATA_POST = json.dumps({"email": EMAIL, "password": PASSWORD})
LOGIN_URL = "/api/login/"


@pytest.mark.django_db
def test_obtain_token(create_user, client) -> None:
    user = create_user
    request_login = client.post(LOGIN_URL, DATA_POST, content_type=CONTENT_TYPE_JSON)
    decode_access_token = jwt.decode(request_login.json()["access"], verify=False)
    assert request_login.status_code == status.HTTP_201_CREATED
    assert decode_access_token["user_id"] == user.pk
    assert decode_access_token["user"]["email"] == EMAIL


@pytest.mark.django_db
def test_obtain_token_bad_password_or_email(client, create_user) -> None:
    request_login_bad_password = client.post(
        LOGIN_URL,
        json.dumps({"email": EMAIL, "password": PASSWORD + str("bad")}),
        content_type=CONTENT_TYPE_JSON,
    )
    request_login_bad_email = client.post(
        LOGIN_URL,
        json.dumps({"email": EMAIL + str("bad"), "password": PASSWORD}),
        content_type=CONTENT_TYPE_JSON,
    )
    assert request_login_bad_email.json() == request_login_bad_password.json()
    assert request_login_bad_password.status_code == status.HTTP_401_UNAUTHORIZED
    assert request_login_bad_email.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        request_login_bad_email.json()["message"]
        == "No active account found with the given credentials"
    )


@pytest.mark.django_db
def test_obtain_token_user_is_not_active(client, create_user) -> None:
    user = create_user
    user.is_active = False
    user.save()
    request_login = client.post(LOGIN_URL, DATA_POST, content_type=CONTENT_TYPE_JSON)
    assert request_login.status_code == status.HTTP_401_UNAUTHORIZED
    assert request_login.json()["message"] == "No active account found with the given credentials"
