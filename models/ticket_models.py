from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TicketProperties(BaseModel):
    hs_pipeline: str = Field(..., alias="hs_pipeline")
    hs_pipeline_stage: str = Field(..., alias="hs_pipeline_stage")
    hs_ticket_priority: Optional[str] = Field(None, alias="hs_ticket_priority")
    subject: str
    content: Optional[str] = None

    class Config:
        extra = "allow"

class HubSpotTicketOutput(BaseModel):
    id: str
    properties: Dict[str, Any]
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    archived: bool
