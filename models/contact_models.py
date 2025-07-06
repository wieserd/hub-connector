from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class ContactProperties(BaseModel):
    email: EmailStr
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None

    class Config:
        extra = "allow"

class HubSpotContactOutput(BaseModel):
    id: str
    properties: Dict[str, Any]
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    archived: bool
