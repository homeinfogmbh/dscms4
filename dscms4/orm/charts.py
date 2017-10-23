"""Object Relational Mappings"""


class LocalPublicTtransportChart(Model, Chart):
    """Local public transport chart."""

    class Meta:
        db_table = 'chart_local_public_transport'


class NewsChart(Model, Chart):
    """Chart to display news."""

    class Meta:
        db_table = 'chart_news'

    localization = CharField(255, null=True, default=None)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new news chart from the
        provided JSON compliant dictionary.
        """
        chart = super().from_dict(dictionary)
        chart.localization = dictionary.get('localization')
        chart.save()
        return chart

    def to_dict(self):
        """Converts the chart record into a JSON compliant dictionary."""
        dictionary = super().to_dict()

        if self.localization is not None:
            dictionary['localization'] = self.localization

        return dictionary


class QuotesChart(Model, Chart):
    """Chart for quotations."""

    class Meta:
        db_table = 'chart_quotes'

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart."""
        chart = super().from_dict(dictionary)
        chart.save()
        return chart


class VideoChart(Model, Chart):
    """A chart that may contain images and texts."""

    class Meta:
        db_table = 'chart_video'

    video = ForeignKeyField(
        MediaFile, db_column='video', null=True, default=None)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.video = dictionary['video']
        chart.save()
        return chart

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['video'] = self.video.id
        return dictionary


class GuessPictureChart(Model, Chart):
    """Chart for guessing pictures."""

    class Meta:
        db_table = 'chart_guess_picture'

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.save()
        return chart


class WeatherChart(Model, Chart):
    """Weather data."""

    class Meta:
        db_table = 'chart_weather'

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.save()
        return chart
