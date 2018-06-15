"""Terminal presentation."""

from dscms4 import dom
from dscms4.content.terminal.charts import accumulated_charts
from dscms4.content.terminal.configuration import first_configuration
from dscms4.content.terminal.menu import accumulated_menus

__all__ = ['presentation']


def _presentation_xml(terminal):
    """Returns an XML dom presentation."""

    xml = dom.presentation()
    xml.customer = terminal.customer.id
    xml.tid = terminal.tid
    xml.configuration = first_configuration(terminal).to_dom()
    xml.chart = [chart.to_dom() for _, chart in accumulated_charts(terminal)]
    xml.menu = [menu.to_dom() for _, menu in accumulated_menus(terminal)]
    return xml


def _presentation_json(terminal):
    """Returns a JSON presentation."""

    return {
        'customer': terminal.customer.id,
        'tid': terminal.tid,
        'charts': [
            chart.to_dict() for _, chart in accumulated_charts(terminal)],
        'configuration': first_configuration(terminal).to_dict(),
        'menus': [menu.to_dict() for _, menu in accumulated_menus(terminal)]}


def presentation(terminal, xml=False):
    """Generates a terminal configuration dictionary."""

    if xml:
        return _presentation_xml(terminal)

    return _presentation_json(terminal)
