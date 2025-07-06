from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Type, Any
from hubspot_client import HubSpotClient
from models.api_response_model import APIResponse
import logging

logger = logging.getLogger(__name__)

def create_crud_router(
    object_type: str,
    create_schema: Type[BaseModel],
    response_schema: Type[BaseModel],
    search_property: str = None
) -> APIRouter:
    router = APIRouter()
    hubspot_client = HubSpotClient()

    @router.post(f"/{object_type}", response_model=APIResponse, status_code=status.HTTP_200_OK)
    async def create_or_update_object(data: create_schema):
        """
        Creates a new HubSpot object or updates an existing one.
        """
        try:
            existing_object = None
            if search_property and getattr(data, search_property, None):
                existing_object = await hubspot_client.search_object(
                    object_type,
                    search_property,
                    getattr(data, search_property),
                    response_schema
                )

            if existing_object:
                updated_object = await hubspot_client.update_object(
                    object_type,
                    existing_object.id,
                    data.dict(exclude_unset=True, by_alias=True),
                    response_schema
                )
                return APIResponse(
                    status="success",
                    message=f"{object_type.capitalize()} updated successfully",
                    **{f"hubspot_{object_type}_id": updated_object.id},
                    action="updated"
                )
            else:
                new_object = await hubspot_client.create_object(
                    object_type,
                    data.dict(by_alias=True),
                    response_schema
                )
                return APIResponse(
                    status="success",
                    message=f"{object_type.capitalize()} created successfully",
                    **{f"hubspot_{object_type}_id": new_object.id},
                    action="created"
                )
        except HTTPException as e:
            logger.error(f"HTTPException in {object_type} POST: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in {object_type} POST: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")

    @router.get(f"/{object_type}/{{object_id}}", response_model=response_schema, status_code=status.HTTP_200_OK)
    async def get_object(object_id: str):
        """
        Retrieves a HubSpot object by its ID.
        """
        try:
            obj = await hubspot_client.get_object_by_id(object_type, object_id, response_schema)
            if not obj:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{object_type.capitalize()} not found")
            return obj
        except HTTPException as e:
            logger.error(f"HTTPException in {object_type} GET: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in {object_type} GET: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")

    return router
