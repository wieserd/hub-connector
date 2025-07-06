import pytest
from httpx import AsyncClient
from main import app
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_create_contact_success(mock_hubspot_client):
    mock_hubspot_client.search_object.return_value = None
    mock_hubspot_client.create_object.return_value.id = "new_contact_id"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/contacts",
            json={
                "email": "test@example.com",
                "firstname": "Test",
                "lastname": "User"
            }
        )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["action"] == "created"
    assert response.json()["hubspot_contact_id"] == "new_contact_id"
    mock_hubspot_client.search_object.assert_called_once()
    mock_hubspot_client.create_object.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_success(mock_hubspot_client):
    mock_hubspot_client.search_object.return_value.id = "existing_contact_id"
    mock_hubspot_client.update_object.return_value.id = "existing_contact_id"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/contacts",
            json={
                "email": "test@example.com",
                "firstname": "Updated"
            }
        )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["action"] == "updated"
    assert response.json()["hubspot_contact_id"] == "existing_contact_id"
    mock_hubspot_client.search_object.assert_called_once()
    mock_hubspot_client.update_object.assert_called_once()

@pytest.mark.asyncio
async def test_get_contact_success(mock_hubspot_client):
    mock_hubspot_client.get_object_by_id.return_value.id = "contact_123"
    mock_hubspot_client.get_object_by_id.return_value.properties = {"email": "test@example.com"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/contacts/contact_123")

    assert response.status_code == 200
    assert response.json()["id"] == "contact_123"
    assert response.json()["properties"]["email"] == "test@example.com"
    mock_hubspot_client.get_object_by_id.assert_called_once()

@pytest.mark.asyncio
async def test_get_contact_not_found(mock_hubspot_client):
    mock_hubspot_client.get_object_by_id.return_value = None

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/contacts/nonexistent_id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Contacts not found"
    mock_hubspot_client.get_object_by_id.assert_called_once()

# Similar tests for companies and tickets would follow the same pattern

@pytest.mark.asyncio
async def test_create_association_success(mock_hubspot_client):
    mock_hubspot_client.create_association.return_value = {}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/associations",
            json={
                "from_object_type": "contact",
                "from_object_id": "123",
                "to_object_type": "company",
                "to_object_id": "456",
                "association_type_id": "279"
            }
        )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Association created successfully"
    mock_hubspot_client.create_association.assert_called_once()

@pytest.mark.asyncio
async def test_get_associations_success(mock_hubspot_client):
    mock_hubspot_client.get_associations.return_value = {"results": [{"id": "456", "type": "company"}]}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/associations/contact/123/company")

    assert response.status_code == 200
    assert response.json()["results"][0]["id"] == "456"
    mock_hubspot_client.get_associations.assert_called_once()

@pytest.mark.asyncio
async def test_receive_hubspot_webhook_success():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/webhooks/hubspot",
            json=[
                {
                    "eventId": 1,
                    "subscriptionId": 1,
                    "portalId": 1,
                    "appId": 1,
                    "occurredAt": "2023-01-01T00:00:00.000Z",
                    "subscriptionType": "contact.propertyChange",
                    "attemptNumber": 1,
                    "objectId": 1,
                    "changeFlag": "NEW",
                    "changeSource": "CRM",
                    "propertyName": "email",
                    "propertyValue": "test@example.com",
                    "rawBody": "{}"
                }
            ]
        )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Received 1 events"
