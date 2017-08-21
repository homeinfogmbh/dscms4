"""Content assignments"""

from peewee import Model, ForeignKeyField

from homeinfo.terminals.orm import Terminal

from .common import CustomerModel
from .groups import Group
from .charts import LocalPublicTtransportChart, NewsChart, QuotesChart, \
    VideoChart, HTMLChart, FacebookChart, GuessPictureChart, WeatherChart

__all__ = ['Content', 'TerminalContent', 'GroupContent', 'MODELS']


class Content(CustomerModel):
    """Content assigned to something"""

    local_public_transport_chart = ForeignKeyField(
        LocalPublicTtransportChart, db_column='local_public_transport_chart',
        null=True, default=None)
    news_chart = ForeignKeyField(
        NewsChart, db_column='news_chart', null=True, default=None)
    quotes_chart = ForeignKeyField(
        QuotesChart, db_column='quotes_chart', null=True, default=None)
    video_chart = ForeignKeyField(
        VideoChart, db_column='video_chart', null=True, default=None)
    html_chart = ForeignKeyField(
        HTMLChart, db_column='html_chart', null=True, default=None)
    facebook_chart = ForeignKeyField(
        FacebookChart, db_column='facebook_chart', null=True, default=None)
    guess_picture_chart = ForeignKeyField(
        GuessPictureChart, db_column='guess_picture_chart', null=True,
        default=None)
    weather_chart = ForeignKeyField(
        WeatherChart, db_column='weather_chart', null=True, default=None)

    @property
    def chart(self):
        """Gets the respective chart"""
        if self.local_public_transport_chart is not None:
            return self.local_public_transport_chart
        elif self.news_chart is not None:
            return self.news_chart
        elif self.quotes_chart is not None:
            return self.quotes_chart
        elif self.video_chart is not None:
            return self.video_chart
        elif self.html_chart is not None:
            return self.html_chart
        elif self.facebook_chart is not None:
            return self.facebook_chart
        elif self.guess_picture_chart is not None:
            return self.guess_picture_chart
        elif self.weather_chart is not None:
            return self.weather_chart
        else:
            raise ValueError('No chart set.')

    @chart.setter
    def chart(cls, chart):
        """Sets the respective charte"""
        content = cls()

        if isinstance(chart, LocalPublicTtransportChart):
            content.local_public_transport_chart = chart
        elif isinstance(chart, NewsChart):
            content.news_chart = chart
        elif isinstance(chart, QuotesChart):
            content.quotes_chart = chart
        elif isinstance(chart, VideoChart):
            content.video_chart = chart
        elif isinstance(chart, HTMLChart):
            content.html_chart = chart
        elif isinstance(chart, FacebookChart):
            content.facebook_chart = chart
        elif isinstance(chart, GuessPictureChart):
            content.guess_picture_chart = chart
        elif isinstance(chart, WeatherChart):
            content.weather_chart = chart
        else:
            raise ValueError('Invalid chart type: {}.'.format(chart))


class TerminalContent(Model, CustomerModel):
    """Content assigned to terminals"""

    class Meta:
        db_table = 'content_terminal'

    terminal = ForeignKeyField(Terminal, db_column='terminal')

    @classmethod
    def add(cls, terminal, chart):
        """Adds the respective chart to the terminal"""
        terminal_content = cls()
        terminal_content.terminal = terminal
        terminal_content.chart = chart
        terminal_content.save()
        return terminal_content


class GroupContent(Model, CustomerModel):
    """Content assigned to terminals"""

    class Meta:
        db_table = 'content_group'

    group = ForeignKeyField(Group, db_column='group')

    @classmethod
    def add(cls, group, chart):
        """Adds the respective chart to the terminal"""
        group_content = cls()
        group_content.group = group
        group_content.chart = chart
        group_content.save()
        return group_content


MODELS = ['TerminalContent', 'GroupContent']
