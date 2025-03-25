from typing import Optional
from typing_extensions import TypedDict


class EventModel(TypedDict):
    title: Optional[str]
    date: Optional[str]
    category: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    link: Optional[str]
