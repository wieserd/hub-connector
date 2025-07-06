import httpx
import logging
from typing import Dict, Any, Optional
from config import settings
from models.contact_models import HubSpotContactOutput
from models.company_models import HubSpotCompanyOutput
from models.ticket_models import HubSpotTicketOutput

logger = logging.getLogger(__name__)

class HubSpotClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.HUBSPOT_PRIVATE_APP_TOKEN}",
            "Content-Type": "application/json"
        }

    def _get_object_url(self, object_type: str) -> str:
        return f"https://api.hubapi.com/crm/v3/objects/{object_type}"

    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=self.headers, **kwargs)
                response.raise_for_status()  # Raise an exception for 4xx/5xx responses
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = f"HubSpot API error: {e.response.status_code} - {e.response.text}"
                logger.error(f"Request failed: {method} {url}, Status: {e.response.status_code}, Response: {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail=error_detail)
            except httpx.RequestError as e:
                error_detail = f"Network error during HubSpot API request: {e}"
                logger.error(f"Request failed: {method} {url}, Error: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

    async def get_object_by_id(self, object_type: str, object_id: str, output_model: Any) -> Optional[Any]:
        get_url = f"{self._get_object_url(object_type)}/{object_id}"
        try:
            response = await self._make_request("GET", get_url)
            return output_model(**response)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def create_object(self, object_type: str, properties: Dict[str, Any], output_model: Any) -> Any:
        create_url = self._get_object_url(object_type)
        payload = {"properties": properties}
        response = await self._make_request("POST", create_url, json=payload)
        return output_model(**response)

    async def update_object(self, object_type: str, object_id: str, properties: Dict[str, Any], output_model: Any) -> Any:
        update_url = f"{self._get_object_url(object_type)}/{object_id}"
        payload = {"properties": properties}
        response = await self._make_request("PATCH", update_url, json=payload)
        return output_model(**response)

    async def search_object(self, object_type: str, property_name: str, property_value: str, output_model: Any) -> Optional[Any]:
        search_url = f"{self._get_object_url(object_type)}/search"
        payload = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": property_name,
                            "operator": "EQ",
                            "value": property_value
                        }
                    ]
                }
            ],
            "limit": 1
        }
        try:
            response = await self._make_request("POST", search_url, json=payload)
            if response and response.get("results"):
                return output_model(**response["results"][0])
            return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def create_association(self, from_object_type: str, from_object_id: str, to_object_type: str, to_object_id: str, association_type_id: str) -> Dict[str, Any]:
        create_url = f"https://api.hubapi.com/crm/v4/associations/{from_object_type}/{to_object_type}/batch/create"
        payload = {
            "inputs": [
                {
                    "from": {"id": from_object_id},
                    "to": {"id": to_object_id},
                    "type": association_type_id
                }
            ]
        }
        response = await self._make_request("POST", create_url, json=payload)
        return response

    async def get_associations(self, object_type: str, object_id: str, to_object_type: str) -> Dict[str, Any]:
        get_url = f"https://api.hubapi.com/crm/v4/objects/{object_type}/{object_id}/associations/{to_object_type}"
        response = await self._make_request("GET", get_url)
        return response
