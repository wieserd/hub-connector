import logging
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List
from hubspot_client import HubSpotClient
from models.api_response_model import APIResponse

router = APIRouter()
hubspot_client = HubSpotClient()
logger = logging.getLogger(__name__)

class AssociationCreate(BaseModel):
    from_object_type: str
    from_object_id: str
    to_object_type: str
    to_object_id: str
    association_type_id: str

class AssociationResponse(BaseModel):
    from_object_id: str
    to_object_id: str
    association_type_id: str

@router.post("/associations", response_model=APIResponse, status_code=status.HTTP_200_OK)
async def create_association(association_data: AssociationCreate):
    """
    Creates an association between two HubSpot objects.
    """
    try:
        response = await hubspot_client.create_association(
            association_data.from_object_type,
            association_data.from_object_id,
            association_data.to_object_type,
            association_data.to_object_id,
            association_data.association_type_id
        )
        return APIResponse(
            status="success",
            message="Association created successfully",
            action="created"
        )
    except HTTPException as e:
        logger.error(f"HTTPException in create_association: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in create_association: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")

@router.get("/associations/{object_type}/{object_id}/{to_object_type}", status_code=status.HTTP_200_OK)
async def get_associations(object_type: str, object_id: str, to_object_type: str):
    """
    Retrieves associations for a given HubSpot object.
    """
    try:
        response = await hubspot_client.get_associations(object_type, object_id, to_object_type)
        return response
    except HTTPException as e:
        logger.error(f"HTTPException in get_associations: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_associations: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
