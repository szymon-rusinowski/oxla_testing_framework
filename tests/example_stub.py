import httpx
import pytest
from pytest_mock import MockFixture

API_PREFIX_V1 = "/api/v1"


def test_get_stub_user(client, auth_headers_admin):
    with client as client:
        response = client.get(
            API_PREFIX_V1 + "/soileo_api/users", headers=auth_headers_admin
        )
    print(response.json())
    assert response.status_code == 200
    assert response.json()[0]["username"] == "admin"


@pytest.mark.asyncio
async def test_on_add_user(client, mocker: MockFixture, auth_headers_admin):
    valid_user_data = {
        "email": "test2@qzsolutions.pl",
        "username": "fake_user",
        "password": "Test123",
    }
    mocker.patch("httpx.AsyncClient.post")
    httpx.AsyncClient.post.return_value = httpx.Response(status_code=201)
    with client as client:
        response = client.post(
            API_PREFIX_V1 + "/soileo_api/add_user",
            json=valid_user_data,
            headers=auth_headers_admin,
        )
        get_all_users = client.get(
            API_PREFIX_V1 + "/soileo_api/users", headers=auth_headers_admin
        )
    assert response.status_code == 200
    assert get_all_users.json()[0]["username"] == "admin"
    assert get_all_users.json()[1]["username"] == "fake_user"
    assert get_all_users.status_code == 200


def test_on_invalid_add_user(client, auth_headers_admin):
    invalid_user_data = {"email": "test2@qzsolutions.pl", "username": "fake_user"}
    with client as client:
        response = client.post(
            API_PREFIX_V1 + "/soileo_api/add_user",
            json=invalid_user_data,
            headers=auth_headers_admin,
        )
    assert response.status_code == 422


def test_on_add_user_if_exist(client, auth_headers_admin):
    valid_user_data = {
        "email": "test@qzsolutions.pl",
        "username": "admin",
        "password": "Test123",
    }
    with client as client:
        response = client.post(
            API_PREFIX_V1 + "/soileo_api/add_user",
            json=valid_user_data,
            headers=auth_headers_admin,
        )
    print(response.json())
    assert response.json() == {"detail": "Email or Username Already exists"}
    assert response.status_code == 400


def test_on_login(client):
    valid_user_login_data = {
        "username": "admin",
        "password": "Test123",
        "grant_type": "password",
    }
    with client as client:
        response = client.post(
            API_PREFIX_V1 + "/soileo_api/login",
            data=valid_user_login_data,
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_on_current_user(client):
    valid_user_login_data = {
        "username": "admin",
        "password": "Test123",
        "grant_type": "password",
    }
    with client as client:
        response = client.post(
            API_PREFIX_V1 + "/soileo_api/login",
            data=valid_user_login_data,
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        response_current_user = client.get(
            API_PREFIX_V1 + "/soileo_api/current_user",
            headers={"Authorization": "Bearer " + response.json()["access_token"]},
        )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response_current_user.json()["username"] == "admin"
    assert response_current_user.status_code == 200


@pytest.mark.asyncio
async def test_on_delete_user(client, mocker: MockFixture, auth_headers_admin):
    valid_user_data = {
        "email": "test2@qzsolutions.pl",
        "username": "fake_user",
        "password": "Test123",
    }
    mocker.patch("httpx.AsyncClient.post")
    httpx.AsyncClient.post.return_value = httpx.Response(status_code=200)
    mocker.patch("httpx.AsyncClient.delete")
    httpx.AsyncClient.delete.return_value = httpx.Response(status_code=200)
    username_to_delete = "fake_user"

    with client as client:
        response = client.post(
            API_PREFIX_V1 + "/soileo_api/add_user",
            json=valid_user_data,
            headers=auth_headers_admin,
        )
        get_all_users_beofre_remove = client.get(
            API_PREFIX_V1 + "/soileo_api/users", headers=auth_headers_admin
        )
        response_on_remove = client.delete(
            API_PREFIX_V1 + "/soileo_api/user/" + username_to_delete,
            headers=auth_headers_admin,
        )
        get_all_users_after_remove = client.get(
            API_PREFIX_V1 + "/soileo_api/users", headers=auth_headers_admin
        )

    assert response.status_code == 200
    assert get_all_users_beofre_remove.json()[0]["username"] == "admin"
    assert get_all_users_beofre_remove.json()[1]["username"] == "fake_user"
    assert get_all_users_beofre_remove.status_code == 200
    assert response_on_remove.status_code == 200
    assert len(get_all_users_after_remove.json()) == 1
    assert get_all_users_after_remove.status_code == 200


def test_on_unauthorized_access_to_route(client, add_common_user, auth_headers_user):
    with client as client:
        response = client.get(
            API_PREFIX_V1 + "/soileo_api/users", headers=auth_headers_user
        )
    print(response.json())
    assert response.status_code == 403
    assert response.json()["detail"] == "Operation not permitted"
