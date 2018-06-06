"""Terminal presentation."""

from dscms4 import dom
from dscms4.content.terminal.charts import accumulated_charts
from dscms4.content.terminal.configuration import accumulated_configurations
from dscms4.content.terminal.menu import accumulated_menus

__all__ = ['presentation']


def _presentation_xml(terminal):
    """Returns an XML dom presentation."""

    xml = dom.presentation()
    xml.configuration = [
        configuration.to_dom() for _, configuration in
        accumulated_configurations(terminal)]
    xml.chart = [chart.to_dom() for _, chart in accumulated_charts(terminal)]
    xml.menu = [menu.to_dom() for _, menu in accumulated_menus(terminal)]
    return xml


def presentation(terminal, xml=False):
    """Generates a terminal configuration dictionary."""

    if xml:
        return _presentation_xml(terminal)

    return {
        'customer': terminal.customer.id,
        'tid': terminal.tid,
        'charts': [
            chart.to_dict() for _, chart in accumulated_charts(terminal)],
        'configurations': [
            configuration.to_dict() for _, configuration in
            accumulated_configurations(terminal)],
        'menus': [menu.to_dict() for _, menu in accumulated_menus(terminal)]}
