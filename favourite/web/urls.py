from tornado.web import RequestHandler
from typing import List, Tuple

from web.handlers import (
    PingHandler,
    AddToFavourite,
    RemoveFromFavourite,
    GetAllFavourite,
    CheckIfFavourite
)

ping_url = (r'/ping/', PingHandler)

custom_urls = [
    (r'/add-to-favourite/', AddToFavourite),
    (r'/remove-from-favourite/', RemoveFromFavourite),
    (r'/get-all-favourite/', GetAllFavourite),
    (r'/check-if-favourite/', CheckIfFavourite),
]


def get_all_urls() -> List[Tuple[str, RequestHandler]]:
    return custom_urls + [ping_url]
