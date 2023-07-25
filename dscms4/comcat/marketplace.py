"""Customer-side administration of the market place service."""

from his import CUSTOMER, authenticated, authorized
from marketplace import ERRORS, get_offer, get_offers, get_image
from wsgilib import Binary, JSON, JSONMessage


__all__ = ["ROUTES", "ERRORS"]


@authenticated
@authorized("comcat")
def list_() -> JSON:
    """Lists offers."""

    return JSON([offer.to_json() for offer in get_offers(customer=CUSTOMER.id)])


@authenticated
@authorized("comcat")
def get(ident: int) -> JSON:
    """Get an offer."""

    return JSON(get_offer(ident, customer=CUSTOMER.id).to_json())


@authenticated
@authorized("comcat")
def delete(ident: int) -> JSONMessage:
    """Deletes an offer."""

    get_offer(ident, customer=CUSTOMER.id).delete_instance()
    return JSONMessage("Offer deleted.", status=200)


@authenticated
@authorized("comcat")
def get_img(ident: int) -> Binary:
    """Returns an offer image."""

    return Binary(get_image(ident, customer=CUSTOMER.id).file.bytes)


@authenticated
@authorized("comcat")
def del_img(ident: int) -> JSONMessage:
    """Deletes an offer image."""

    get_image(ident, customer=CUSTOMER.id).delete_instance()
    return JSONMessage("Image deleted.", status=200)


ROUTES = [
    ("GET", "/marketplace", list_),
    ("GET", "/marketplace/<int:ident>", get),
    ("DELETE", "/marketplace/<int:ident>", delete),
    ("GET", "/marketplace/image/<int:ident>", get_img),
    ("DELETE", "/marketplace/image/<int:ident>", del_img),
]
