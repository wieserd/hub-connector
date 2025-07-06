import pytest
from unittest.mock import AsyncMock, patch
from hubspot_client import HubSpotClient
from models.contact_models import HubSpotContactOutput
from models.company_models import HubSpotCompanyOutput
from models.ticket_models import HubSpotTicketOutput
from httpx import HTTPStatusError, Request, Response

@pytest.fixture
def hubspot_client_instance():
    return HubSpotClient()

@pytest.mark.asyncio
async def test_create_object_success(hubspot_client_instance):
    with patch('httpx.AsyncClient.request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = {
            "id": "123",
            "properties": {"email": "test@example.com"},
            "createdAt": "2023-01-01T00:00:00Z",
            "updatedAt": "2023-01-01T00:00:00Z",
            "archived": False
        }
        mock_request.return_value.raise_for_status.return_value = None

        properties = {"email": "test@example.com"}
        result = await hubspot_client_instance.create_object("contacts", properties, HubSpotContactOutput)

        assert result.id == "123"
        assert result.properties["email"] == "test@example.com"
        mock_request.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_by_id_success(hubspot_client_instance):
    with patch('httpx.AsyncClient.request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = {
            "id": "123",
            "properties": {"email": "test@example.com"},
            "createdAt": "2023-01-01T00:00:00Z",
            "updatedAt": "2023-01-01T00:00:00Z",
            "archived": False
        }
        mock_request.return_value.raise_for_status.return_value = None

        result = await hubspot_client_instance.get_object_by_id("contacts", "123", HubSpotContactOutput)

        assert result.id == "123"
        mock_request.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_by_id_not_found(hubspot_client_instance):
    with patch('httpx.AsyncClient.request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.raise_for_status.side_effect = HTTPStatusError(
            "Not Found", request=Request(method="GET", url="http://test.com"), response=Response(404)
        )

        result = await hubspot_client_instance.get_object_by_id("contacts", "nonexistent", HubSpotContactOutput)

        assert result is None
        mock_request.assert_called_once()

@pytest.mark.asyncio
async def test_update_object_success(hubspot_client_instance):
    with patch('httpx.AsyncClient.request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = {
            "id": "123",
            "properties": {"email": "updated@example.com"},
            "createdAt": "2023-01-01T00:00:00Z",
            "updatedAt": "2023-01-01T00:00:00Z",
            "archived": False
        }
        mock_request.return_value.raise_for_status.return_value = None

        properties = {"email": "updated@example.com"}
        result = await hubspot_client_instance.update_object("contacts", "123", properties, HubSpotContactOutput)

        assert result.id == "123"
        assert result.properties["email"] == "updated@example.com"
        mock_request.assert_called_once()

@pytest.mark.asyncio
async def test_search_object_success(hubspot_client_instance):
    with patch('httpx.AsyncClient.request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = {"results": [
            {
                "id": "123",
                "properties": {"email": "search@example.com"},
                "createdAt": "2023-01-01T00:00:00Z",
                "updatedAt": "2023-01-01T00:00:00Z",
                "archived": False
            }
        ]}
        mock_request.return_value.raise_for_status.return_value = None

        result = await hubspot_client_instance.search_object("contacts", "email", "search@example.com", HubSpotContactOutput)

        assert result.id == "123"
        assert result.properties["email"] == "search@example.com"
        mock_request.assert_called_once()

@pytest.mark.asyncio
async def test_search_object_not_found(hubspot_client_instance):
    with patch('httpx.AsyncClient.request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = {"results": []}
        mock_request.return_value.raise_for_status.return_value = None

        result = await hubspot_client_instance.search_object("contacts", "email", "nonexistent@example.com", HubSpotContactOutput)

        assert result is None
        mock_request.assert_called_once()

@pytest.mark.asyncio
async def test_create_association_success(hubspot_client_instance):
    with patch('httpx.AsyncClient.request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = {}
        mock_request.return_value.raise_for_status.return_value = None

        result = await hubspot_client_instance.create_association("contact", "1", "company", "2", "279")

        assert result == {}
        mock_request.assert_called_once()

@pytest.mark.asyncio
async def test_get_associations_success(hubspot_client_instance):
    with patch('httpx.AsyncClient.request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value.json.return_value = {"results": [{"id": "2", "type": "company"}]}
        mock_request.return_value.raise_for_status.return_value = None

        result = await hubspot_client_instance.get_associations("contact", "1", "company")

        assert result["results"][0]["id"] == "2"
        mock_request.assert_called_once()
