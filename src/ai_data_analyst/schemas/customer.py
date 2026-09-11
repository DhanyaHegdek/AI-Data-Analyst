from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

#CustomerCreate Used when the client sends data:
class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    city: str | None = None

#CustomerResponse Used when our API sends data back:
class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    city: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)