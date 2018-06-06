"""Terminal presentation."""

from dscms4.content.terminal.charts import accumulated_charts
from dscms4.content.terminal.configuration import accumulated_configurations
from dscms4.content.terminal.menu import accumulated_menus

__all__ = ['presentation']


def presentation(terminal):
    """Generates a terminal configuration dictionary."""

    return {
        'customer': terminal.customer.id,
        'tid': terminal.tid,
        'charts': [
            chart.to_dict() for _, chart in accumulated_charts(terminal)],
        'configurations': [
            configuration.to_dict() for _, configuration in
            accumulated_configurations(terminal)],
        'menus': [menu.to_dict() for _, menu in accumulated_menus(terminal)]}
