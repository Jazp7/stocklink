from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

# ProviderBase: The foundation for all our Provider schemas.
# We put common fields here to avoid repeating ourselves.
class ProviderBase(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None

# ProviderCreate: Used when the frontend sends us data to create a NEW provider.
# It's identical to ProviderBase for now, but in the future, it could have 
# extra validation (like password confirmation if we had accounts).
class ProviderCreate(ProviderBase):
    pass

# ProviderUpdate: Used when we want to UPDATE an existing provider.
# All fields are optional here because you might only want to change the phone number, 
# not the entire provider profile.
class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None

# Provider: This is what a provider looks like once it's in our database.
# It includes the 'id' and timestamps that the database creates for us.
class Provider(ProviderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # This 'model_config' tells Pydantic to treat database rows (which behave like objects) 
    # as if they were dictionaries, so it can easily convert them to JSON.
    model_config = ConfigDict(from_attributes=True)

# ProviderResponse: This follows the "Consistent JSON" rule in AGENTS.md.
# Every successful response will look like: { "success": true, "data": { ... } }
class ProviderResponse(BaseModel):
    success: bool = True
    data: Provider

# ProviderListResponse: Same as above, but for when we return a LIST of providers.
class ProviderListResponse(BaseModel):
    success: bool = True
    data: List[Provider]
