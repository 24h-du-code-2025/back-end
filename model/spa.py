from typing_extensions import TypedDict


class SpaModel(TypedDict):
    name: str
    description: str
    location: str
    phone_number: str
    email: str
    opening_hours: str
