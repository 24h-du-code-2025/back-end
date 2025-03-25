from langchain_core.tools import tool
import requests

from config import Config
from model import (
    ReservationModel,
    GetReservationsModel,
    UpdateReservationsModel,
    PatchReservationsModel,
    ReservationDisplayModel
)
from utils import add_structured_message


API_HEADERS = Config.API_HEADERS
HOTEL_API_URL = Config.HOTEL_API_URL


@tool
def add_reservation(reservation: ReservationModel):
    """Create a restaurant reservation"""
    return requests.post(HOTEL_API_URL + "/api/reservations/", json=reservation.dict(), headers=API_HEADERS).text


@tool
def get_reservation(reservation_id: int):
    """Get information about a restaurant reservation"""
    return requests.get(HOTEL_API_URL + f"/api/reservations/{reservation_id}/", headers=API_HEADERS).text


@tool
def get_reservations(params: GetReservationsModel):
    """Get information about client reservations"""
    return requests.get(HOTEL_API_URL + f"/api/reservations/", params=params, headers=API_HEADERS).text


@tool
def update_reservation(reservation_id: int, params: UpdateReservationsModel):
    """Update reservation information"""
    return requests.put(HOTEL_API_URL + f"/api/reservations/{reservation_id}/", json=params.dict(), headers=API_HEADERS).text


@tool
def patch_reservation(reservation_id: int, params: PatchReservationsModel):
    """Partially update reservation information"""
    return requests.patch(HOTEL_API_URL + f"/api/reservations/{reservation_id}/", json=params.dict(), headers=API_HEADERS).text


@tool
def list_reservations():
    """list all reservations in the restaurants"""
    return requests.get(HOTEL_API_URL+"/api/reservations/", headers=API_HEADERS).text


@tool
def delete_reservation(reservation_id: int):
    """list all available spas arround the hotel"""
    return requests.delete(HOTEL_API_URL + f"/api/reservations/{reservation_id}/", headers=API_HEADERS).text


@tool
def display_reservation_data(
        reservation: ReservationDisplayModel
):
    """When a reservation is created or the user ask about the details of a reservation, always respond using this tool"""
    add_structured_message("reservation_details", reservation.dict())
    return "__end__"
