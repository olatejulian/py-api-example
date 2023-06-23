from fastapi.testclient import TestClient

from .bootstrap import fastapi_bootstrap
from .dependency_injector import celery_event_bus_factory, fake_event_bus_factory

app = fastapi_bootstrap()

app.dependency_overrides[celery_event_bus_factory] = fake_event_bus_factory

client = TestClient(app)


def test_signup():
    # given
    request_body = {
        "name": "John Doe",
        "email": "john.doe@email.com",
        "password": "JohnDoePassword",
    }

    # when
    response = client.post("/signup", json=request_body)

    # then
    assert response.status_code == 200
    assert response.json() == {"success": True}
