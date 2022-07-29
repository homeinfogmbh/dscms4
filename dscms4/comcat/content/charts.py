"""Management of charts assigned to ComCat accounts."""

from flask import request
from peewee import Select

from cmslib import CHART_TYPE, BaseChart, get_base_chart, get_chart
from comcatlib import User, UserBaseChart
from his import CUSTOMER, authenticated, authorized
from mdb import Tenement
from wsgilib import JSON, JSONMessage

from dscms4.comcat.functions import get_user


__all__ = ['ROUTES']


def list_ubc(user: int = None) -> Select:
    """Yields the user's base charts of the
    current customer for the respective user.
    """

    condition = Tenement.customer == CUSTOMER.id
    condition &= BaseChart.trashed == 0

    if user is not None:
        condition &= User.id == user

    return UserBaseChart.select(cascade=True).where(condition)


def get_ubc(ident: int) -> UserBaseChart:
    """Returns a UserBaseChart by its id and customer context."""

    return list_ubc().where(UserBaseChart.id == ident).get()


@authenticated
@authorized('comcat')
def get(ident: int) -> JSON:
    """Returns the respective UserBaseChart."""

    return JSON(get_ubc(ident).to_json(chart=True))


@authenticated
@authorized('comcat')
def list_(user: int) -> JSON:
    """Returns a list of UserBaseCharts of the given user."""

    return JSON([ubc.to_json(chart=True) for ubc in list_ubc(user)])


@authenticated
@authorized('comcat')
def add() -> JSONMessage:
    """Adds the chart to the respective user."""

    user = get_user(request.json.pop('user'), CUSTOMER.id)
    base_chart = get_base_chart(request.json.pop('baseChart'), CUSTOMER.id)
    user_base_chart = UserBaseChart.from_json(request.json, user, base_chart)
    user_base_chart.save()
    return JSONMessage(
        'User base chart added.', id=user_base_chart.id, status=201
    )


@authenticated
@authorized('comcat')
def patch(ident: int) -> JSONMessage:
    """Alter the respective user <-> base chart mapping."""

    user_base_chart = get_ubc(ident)
    user_base_chart.patch_json(request.json)
    user_base_chart.save()
    return JSONMessage(
        'User base chart patched.', id=user_base_chart.id, status=200
    )


@authenticated
@authorized('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes the chart from the respective user."""

    user_base_chart = get_ubc(ident)
    user_base_chart.delete_instance()
    return JSONMessage(
        'User base chart deleted.', id=user_base_chart.id, status=200
    )


@authenticated
@authorized('comcat')
def chart_user_base_charts(ident: int) -> JSON:
    """Returns a list of UserBaseChart for the given chart."""

    chart = get_chart(ident, CUSTOMER.id, CHART_TYPE)
    user_base_charts = UserBaseChart.select().where(
        UserBaseChart.base_chart == chart.base)
    users_base_charts = [ubc.to_json() for ubc in user_base_charts]
    return JSON(users_base_charts)


ROUTES = (
    ('GET', '/content/user/base_chart/<int:ident>', get),
    ('GET', '/content/user/<int:user>/base_chart', list_),
    ('POST', '/content/user/base_chart', add),
    ('PATCH', '/content/user/base_chart/<int:ident>', patch),
    ('DELETE', '/content/user/base_chart/<int:ident>', delete),
    ('GET', '/content/user/user_base_charts/<int:ident>',
     chart_user_base_charts)
)
