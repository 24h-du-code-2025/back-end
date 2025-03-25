from pydantic import BaseModel, Field
from typing import Optional


class CreateClientModel(BaseModel):
    name: str = Field(description="First and last name of the client")
    phone_number: str = Field(description="phone number of the client")
    room_number: Optional[str] = Field(description="the number of the room")
    special_requests: Optional[str] = Field(
        description="any additional info or special request about the client and his reservation",
        examples=["I need a double bed", "I will left at 10 o clock"]
    )


class UpdateClientModel(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    room_number: Optional[str]
    special_requests: Optional[str]
    