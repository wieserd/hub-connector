from pydantic import BaseModel
from typing import Optional

class APIResponse(BaseModel):
    status: str
    message: str
    hubspot_contact_id: Optional[str] = None
    hubspot_company_id: Optional[str] = None
    hubspot_ticket_id: Optional[str] = None
    action: Optional[str] = None
