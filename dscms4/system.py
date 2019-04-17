"""Digital signage systems-related requests."""

from flask import request

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.functions.system import with_system
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.orm.charts import BaseChart
from cmslib.orm.content.system import SystemBaseChart
from cmslib.orm.content.system import SystemConfiguration
from cmslib.orm.content.system import SystemMenu
from cmslib.orm.settings import Settings
from cmslib.presentation.system import Presentation
from his import CUSTOMER, authenticated, authorized
from terminallib import Deployment, System
from wsgilib import Browser, JSON, XML


__all__ = ['ROUTES']


BROWSER = Browser()


@authenticated
@authorized('dscms4')
def list_():
    """Lists all systems of the respective customer."""

    expression = Deployment.customer == CUSTOMER.id
    settings = Settings.for_customer(CUSTOMER.id)

    if not settings.testing:
        expression &= Deployment.testing == 0

    systems = System.select().join(Deployment).where(expression)

    if BROWSER.wanted:
        if BROWSER.info:
            return BROWSER.pages(systems).to_json()

        return JSON([
            system.to_json(brief=True, cascade=True)
            for system in BROWSER.browse(systems)])

    if 'assoc' in request.args:
        return JSON({
            system.id: SystenContent(system).to_json()
            for system in systems})

    return JSON([
        system.to_json(brief=True, cascade=True) for system in systems])


@authenticated
@authorized('dscms4')
@with_system
def get(system):
    """Returns the respective system."""

    return JSON(system.to_json(brief=True, cascade=True))


@authenticated
@authorized('dscms4')
@with_system
def get_presentation(system):
    """Returns the presentation for the respective system."""

    presentation = Presentation(system)

    try:
        request.args['xml']
    except KeyError:
        return JSON(presentation.to_json())

    try:
        presentation_dom = presentation.to_dom()
    except AmbiguousConfigurationsError:
        return AMBIGUOUS_CONFIGURATIONS
    except NoConfigurationFound:
        return NO_CONFIGURATION_ASSIGNED

    return XML(presentation_dom)


class SystenContent:
    """Represents content of a system."""

    def __init__(self, system):
        """Sets the system."""
        self.system = system

    @property
    def charts(self):
        """Yields the system's charts."""
        for sbc in SystemBaseChart.select().join(BaseChart).where(
                (SystemBaseChart.system == self.system)
                & (BaseChart.trashed == 0)):
            yield sbc.to_json()

    @property
    def configurations(self):
        """Yields the system's configurations."""
        for system_configuration in SystemConfiguration.select().where(
                SystemConfiguration.system == self.system):
            yield system_configuration.to_json()

    @property
    def menus(self):
        """Yields the system's menus."""
        for system_menu in SystemMenu.select().where(
                SystemMenu.system == self.system):
            yield system_menu.to_json()

    def content(self):
        """Returns content."""
        return {
            'charts': list(self.charts),
            'configurations': list(self.configurations),
            'menus': list(self.menus)}

    def to_json(self):
        """Returns the system and its content as a JSON-ish dict."""
        try:
            address = self.system.deployment.address
        except AttributeError:
            address = None

        json = {'address': address.to_json()} if address else {}
        json['content'] = self.content()
        return json


ROUTES = (
    ('GET', '/system', list_),
    ('GET', '/system/<int:ident>', get),
    ('GET', '/system/<int:ident>/presentation', get_presentation)
)
