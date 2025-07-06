import pytest
from unittest.mock import AsyncMock, MagicMock
from hubspot_client import HubSpotClient

@pytest.fixture
def mock_hubspot_client():
    client = AsyncMock(spec=HubSpotClient)
    # Mock common methods that are used across tests
    client.create_object.return_value = MagicMock(id="mock_id", properties={})
    client.update_object.return_value = MagicMock(id="mock_id", properties={})
    client.get_object_by_id.return_value = MagicMock(id="mock_id", properties={})
    client.search_object.return_value = None # Default to not found
    client.create_association.return_value = {}
    client.get_associations.return_value = {"results": []}
    return client
