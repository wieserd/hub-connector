import logging
from fastapi import APIRouter, Request, HTTPException, status
from typing import List, Dict, Any

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhooks/hubspot", status_code=status.HTTP_200_OK)
async def receive_hubspot_webhook(request: Request, events: List[Dict[str, Any]]):
    """
    Receives webhook events from HubSpot.
    
    Note: Full signature verification is not implemented in this basic example.
    In a production environment, you MUST verify the X-HubSpot-Signature header.
    """
    try:
        # For production, implement HubSpot signature verification here:
        # from config import settings
        # import hashlib
        # import hmac
        #
        # signature = request.headers.get("X-HubSpot-Signature")
        # if not signature:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing HubSpot signature")
        #
        # # Reconstruct the string to sign
        # # This depends on the webhook version. For v3, it's usually method + path + body + app_secret
        # # For simplicity, let's assume body is the main part for now.
        # body = await request.body()
        # expected_signature = hmac.new(settings.HUBSPOT_WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
        #
        # if not hmac.compare_digest(signature, expected_signature):
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid HubSpot signature")

        logger.info(f"Received {len(events)} HubSpot webhook events:")
        for event in events:
            logger.info(f"  Event Type: {event.get('eventType')}")
            logger.info(f"  Object Type: {event.get('objectType')}")
            logger.info(f"  Object ID: {event.get('objectId')}")
            logger.info(f"  Change Source: {event.get('changeSource')}")
            logger.info(f"  Change Flag: {event.get('changeFlag')}")
            logger.info(f"  Subscription ID: {event.get('subscriptionId')}")
            logger.info(f"  Portal ID: {event.get('portalId')}")
            logger.info(f"  App ID: {event.get('appId')}")
            logger.info(f"  Occurred At: {event.get('occurredAt')}")
            logger.info(f"  Properties: {event.get('properties')}")
            logger.info("--------------------------------------------------")

        # In a real application, you would process these events here.
        # For example, update your internal database, trigger other integrations, etc.

        return {"status": "success", "message": f"Received {len(events)} events"}
    except HTTPException as e:
        logger.error(f"HTTPException in webhook: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in webhook: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
