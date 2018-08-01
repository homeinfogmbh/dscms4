"""DSCMS4 WSGI handlers for menus."""

from flask import request

from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.menu import NoSuchMenu, InvalidMenuData, MenuAdded, \
    MenuPatched, MenuDeleted
from dscms4.orm.menu import Menu

__all__ = ['get_menu', 'ROUTES']


def get_menu(ident):
    """Returns the respective menu by its ID."""

    try:
        return Menu.get((Menu.customer == CUSTOMER.id) & (Menu.id == ident))
    except Menu.DoesNotExist:
        raise NoSuchMenu()


def get_menus():
    """Yields the menus of the current customer."""

    return Menu.select().where(Menu.customer == CUSTOMER.id)


@authenticated
@authorized('dscms4')
def list_():
    """List menus."""

    return JSON([menu.to_dict() for menu in get_menus()])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective menu."""

    return JSON(get_menu(ident).to_dict())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new menu."""

    try:
        menu = Menu.from_dict(CUSTOMER.id, request.json)
    except ValueError:
        raise InvalidMenuData()

    menu.save()
    return MenuAdded(id=menu.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches the respective menu."""

    menu = get_menu(ident)

    try:
        menu.patch(request.json)
    except ValueError:
        raise InvalidMenuData()

    menu.save()
    return MenuPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes a menu."""

    get_menu(ident).delete_instance()
    return MenuDeleted()


ROUTES = (
    ('GET', '/menu', list_, 'list_menu'),
    ('GET', '/menu/<int:ident>', get, 'get_menu'),
    ('POST', '/menu', add, 'add_menu'),
    ('PATCH', '/menu/<int:ident>', patch, 'patch_menu'),
    ('DELETE', '/menu/<int:ident>', delete, 'delete_menu'))
