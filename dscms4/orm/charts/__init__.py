"""Chart ORM models."""


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
