"""Chart ORM models."""

from sys import stderr

from dscms4.orm.exceptions import OrphanedBaseChart, AmbiguousBaseChart


__all__ = [
    'MODELS',
    'CHARTS',
    'create_tables',
    'chart_of']


MODELS = (
    BaseChart, LocalPublicTtransportChart, NewsChart, QuotesChart, VideoChart,
    ImageTextChart, ChartText, FacebookChart, GuessPictureChart, WeatherChart)
CHARTS = {
    model._meta.db_table.lstrip('chart_'): model
    for model in MODELS if issubclass(model, Chart)}


def create_tables(fail_silently=True):
    """Create the respective tables."""

    for model in MODELS:
        try:
            model.create_table(fail_silently=fail_silently)
        except Exception:
            print('Could not create table for model "{}".'.format(model),
                  file=stderr)


def chart_of(base_chart):
    """Returns the mapped implementation of the respective base chart."""

    matches = []

    for _, cls in CHARTS.items():
        for chart in cls.select().where(cls.base_chart == base_chart):
            matches.append(chart)

    try:
        match, *superfluous = matches
    except ValueError:
        raise OrphanedBaseChart(base_chart) from None
    else:
        if superfluous:
            raise AmbiguousBaseChart(base_chart, matches) from None

        return match
