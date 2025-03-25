from tools.client import (
    get_client,
    get_clients,
    update_client,
    delete_client,
    create_client,
    search_client
)
from tools.event import get_events, display_events
from tools.reservation import (
    add_reservation,
    get_reservation,
    get_reservations,
    list_reservations,
    update_reservation,
    patch_reservation,
    delete_reservation,
    display_reservation_data
)
from tools.restaurant import list_meals, list_restaurants
from tools.spa import display_spa_data, display_spa_list, get_spas
from tools.weather import get_weather


tools = [
    get_weather,
    get_spas,
    display_spa_data,
    display_spa_list,
    list_meals,
    list_reservations,
    list_restaurants,
    add_reservation,
    get_reservation,
    get_reservations,
    update_reservation,
    patch_reservation,
    delete_reservation,
    get_events,
    display_events,
    get_client,
    get_clients,
    update_client,
    delete_client,
    create_client,
    search_client,
    display_reservation_data
]


def get_tools():
    return tools
