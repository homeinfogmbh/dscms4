"""HIS management backend."""

from his import Application

import ccmessenger

from dscms4.comcat import contact_emails
from dscms4.comcat import content
from dscms4.comcat import damage_report
from dscms4.comcat import group
from dscms4.comcat import marketplace
from dscms4.comcat import menu
from dscms4.comcat import messenger
from dscms4.comcat import registration
from dscms4.comcat import reporting
from dscms4.comcat import tenantcalendar
from dscms4.comcat import tenantforum
from dscms4.comcat import tenement
from dscms4.comcat import user
from dscms4.comcat import errors


__all__ = ['APPLICATION']


APPLICATION = Application('comcat')
ROUTES = (
    *contact_emails.ROUTES,
    *content.ROUTES,
    *damage_report.ROUTES,
    *group.ROUTES,
    *marketplace.ROUTES,
    *menu.ROUTES,
    *messenger.ROUTES,
    *registration.ROUTES,
    *reporting.ROUTES,
    *tenantcalendar.ROUTES,
    *tenantforum.ROUTES,
    *tenement.ROUTES,
    *user.ROUTES
)
ERRORS = {
    **errors.ERRORS,
    **marketplace.ERRORS,
    **ccmessenger.ERRORS,
    **tenantcalendar.ERRORS,
    **tenantforum.ERRORS
}


APPLICATION.add_routes(ROUTES)
APPLICATION.register_error_handlers(ERRORS)
