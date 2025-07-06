from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CompanyProperties(BaseModel):
    name: str
    domain: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None

    class Config:
        extra = "allow"

class HubSpotCompanyOutput(BaseModel):
    id: str
    properties: Dict[str, Any]
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    archived: bool
