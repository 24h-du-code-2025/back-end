from pydantic import BaseModel, Field
from typing import Optional


class ReservationDisplayModel(BaseModel):
    restaurant_name: str = Field(description="the name of the restaurant")
    restaurant_location: str = Field(description="address of the restaurant")
    reservation_date: str = Field(description="the date and hour of the reservation")
    meal: str = Field(description="the name of the meal reserved")
    number_of_guests: int = Field(description="the number of guests for the reservation")
    special_requests: Optional[str] = Field(description="Other informations about the reservation")
    
    
class ReservationModel(BaseModel):
    client: int
    date: str
    meal: int
    restaurant: int
    number_of_guests: int
    special_requests: Optional[str]
    
    
class GetReservationsModel(BaseModel):
    client: Optional[int] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    meal: Optional[int] = None
    page: Optional[int] = None
    restaurant: Optional[int] = None
    
    
class UpdateReservationsModel(BaseModel):
    client: int = None
    restaurant: int = None
    date: str = None
    meal: int = None
    number_of_guests: int = None
    special_requests: str = None
    
    
class PatchReservationsModel(BaseModel):
    client: Optional[int] = None
    restaurant: Optional[int] = None
    date: Optional[str] = None
    meal: Optional[int] = None
    number_of_guests: Optional[int] = None
    special_requests: Optional[str] = None
