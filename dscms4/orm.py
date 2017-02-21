"""Object Relational Mappings"""

from datetime import datetime
from peewee import PrimaryKeyField, ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from homeinfo.lib.log import Logger
from filedb import FileProperty
from homeinfo.crm import Customer

from his.orm import module_model


class NoWhitelist(Exception):
    """Indicates that no white list is available"""

    pass


class NoBlacklist(Exception):
    """Indicates that no black list is available"""

    pass


class DSCMS4Model(module_model('dscms4')):
    """Basic ORM model for ComCat"""

    def __init__(self, *args, logger=None, **kwargs):
        """Adds a logger to the instance"""
        super().__init__(*args, **kwargs)

        if logger is None:
            self.logger = Logger(self.__class__.__name__)
        else:
            self.logger = logger.inherit(self.__class__.__name__)

    id = PrimaryKeyField()


class OrganizationUnit(DSCMS4Model):
    """An organizational unit"""

    customer = ForeignKeyField(Customer, db_column='customer')
    parent = ForeignKeyField('self', db_column='parent')
    name = CharField(255)
    annotation = CharField(255, null=True, default=None)


class Schedule(DSCMS4Model):
    """Date / time schedule

    Weekdays are a binary integer:
        All week | Mon | Tue | Wed | Thu | Fri | Sat | Sun
            2^7    2^6   2^5   2^4   2^3   2^2   2^1   2^0
    """

    begin = DateTimeField(null=True)
    end = DateTimeField(null=True)
    weekdays = SmallIntegerField()

    @property
    def all_week(self):
        """Determines whether the schedule runs all week"""
        return self.weekdays >= 128

    @property
    def monday(self):
        """Determines whether the schedule runs on mondays"""
        return self.all_week or self.match_day(0)

    @property
    def tuesday(self):
        """Determines whether the schedule runs on tuesdays"""
        return self.all_week or self.match_day(1)

    @property
    def wednesday(self):
        """Determines whether the schedule runs on wednesdays"""
        return self.all_week or self.match_day(2)

    @property
    def thursday(self):
        """Determines whether the schedule runs on thursdays"""
        return self.all_week or self.match_day(3)

    @property
    def friday(self):
        """Determines whether the schedule runs on fridays"""
        return self.all_week or self.match_day(4)

    @property
    def saturday(self):
        """Determines whether the schedule runs on saturdays"""
        return self.all_week or self.match_day(5)

    @property
    def sunday(self):
        """Determines whether the schedule runs on sundays"""
        return self.all_week or self.match_day(6)

    @property
    def active(self):
        """Determines whether the schedule is currently active"""
        return self.matches(datetime.now())

    def match_day(self, day):
        """Determines whether the schedule
        runs on the respective day
        """
        return self.all_week or self.weekdays & (1 << 6 - day)

    def active_on(self, date):
        """Determines whether the schedule is
        active on the given date or datetime
        """
        if self.match_day(date.weekday()):
            if self.begin is None or self.begin <= date:
                if self.end is None or self.end >= date:
                    return True

        return False


class Chart(DSCMS4Model):
    """Abstract information and message container"""

    title = CharField(255, null=True, default=None)
    text = TextField(null=True, default=None)
    created = DateTimeField()
    begins = DateTimeField(null=True, default=None)
    expires = DateTimeField(null=True, default=None)

    @property
    def active(self):
        """Determines whether the chart is considered active"""
        now = datetime.now()
        match_begins = self.begins is None or self.begins <= now
        match_expires = self.expires is None or self.expires >= now
        return match_begins and match_expires


class RealEstateChart(Chart):
    """Real estate exposé chart"""

    class Meta:
        db_table = 'real_estate_chart'

    qr_code = BooleanField(default=False)
    stretch_images = BooleanField(default=False)
    style = SmallIntegerField()
    contact_image = BooleanField(default=False)
    transition_effect = SmallIntegerField()
    contact = BooleanField(default=False)
    ken_burns = BooleanField(default=False)
    object_number = CharField(255, null=True, default=None)

    def approve(self, real_estate):
        """Approves the respective real estate for this chart"""
        if self.object_number is not None:
            if self.object_number != real_estate.objektnr_extern:
                self.logger.debug(
                    'Excluded real estate "{}" due object '
                    'number filter "{}"'.format(
                        real_estate.objektnr_extern,
                        self.object_number))
                return False

        zip_whitelist = [w.zip_code for w in self.zip_whitelist]

        if zip_whitelist:
            if real_estate.plz not in zip_whitelist:
                self.logger.debug(
                    'Excluded real estate "{}" due to ZIP '
                    'code whitelist "{}"'.format(
                        real_estate.objektnr_extern,
                        zip_whitelist))
                return False

        zip_blacklist = [b.zip_code for b in self.zip_blacklist]

        if zip_blacklist:
            if real_estate.plz in zip_blacklist:
                self.logger.debug(
                    'Excluded real estate "{}" due to ZIP '
                    'code blacklist "{}"'.format(
                        real_estate.objektnr_extern,
                        zip_blacklist))
                return False

        for usage_filter in self._usage_filter:
            if not usage_filter.approve(real_estate):
                return False

        for type_filter in self._type_filter:
            if not type_filter.approve(real_estate):
                return False

        for sale_filter in self._sale_filter:
            if not sale_filter.approve(real_estate):
                return False

        return True


# ### Real estate filters ### #
class RealEstateZIPWhitelist(DSCMS4Model):
    """ZIP code white list for real estate charts"""

    class Meta:
        db_table = 'real_estate_zip_whitelist'

    chart = ForeignKeyField(
        RealEstateChart, db_column='chart',
        realted_name='zip_whitelist')
    zip_code = CharField(255)


class RealEstateZIPBlacklist(RealEstateZIPWhitelist):
    """ZIP code black list for real estate charts"""

    class Meta:
        db_table = 'real_estate_zip_blacklist'

    chart = ForeignKeyField(
        RealEstateChart, db_column='chart',
        realted_name='zip_blacklist')


class RealEstateUsageFilter(DSCMS4Model):
    """Usage type filter for real estates

    XXX: All filters for a chart must match.
    """

    class Meta:
        db_table = 'real_estate_usage_filter'

    chart = ForeignKeyField(
        RealEstateChart, db_column='chart',
        related_name='_usage_filter')
    wohnen = BooleanField(null=True, default=None)
    gewerbe = BooleanField(null=True, default=None)
    anlage = BooleanField(null=True, default=None)
    waz = BooleanField(null=True, default=None)

    def approve(self, real_estate):
        """Approve openimmodb.Immobilie real estate ORM model"""
        if self.wohnen is not None and self.wohnen != real_estate.wohnen:
            self.logger.debug(
                'Excluded real estate "{}".wohnen = {} != {}'.format(
                    real_estate.objektnr_extern,
                    real_estate.wohnen,
                    self.wohnen))
            return False

        if self.gewerbe is not None and self.gewerbe != real_estate.gewerbe:
            self.logger.debug(
                'Excluded real estate "{}".gewerbe = {} != {}'.format(
                    real_estate.objektnr_extern,
                    real_estate.gewerbe,
                    self.gewerbe))
            return False

        if self.anlage is not None and self.anlage != real_estate.anlage:
            self.logger.debug(
                'Excluded real estate "{}".anlage = {} != {}'.format(
                    real_estate.objektnr_extern,
                    real_estate.anlage,
                    self.anlage))
            return False

        if self.waz is not None and self.waz != real_estate.waz:
            self.logger.debug(
                'Excluded real estate "{}".waz = {} != {}'.format(
                    real_estate.objektnr_extern,
                    real_estate.waz,
                    self.waz))
            return False

        return True


class RealEstateTypeFilter(DSCMS4Model):
    """Real estate type filter for real estates

    XXX: All filters for a chart must match.
    """

    class Meta:
        db_table = 'real_estate_type_filter'

    chart = ForeignKeyField(
        RealEstateChart, db_column='chart',
        realted_name='_type_filter')
    klasse = CharField(28)
    typ = CharField(34, null=True, default=None)

    def approve(self, real_estate):
        """Approve openimmodb.Immobilie real estate ORM model"""
        for objektart in real_estate._objektart:
            if objektart.klasse == self.klasse:
                if self.typ is None or objektart.typ == self.typ:
                    return True

        return False


class RealEstateSaleFilter(DSCMS4Model):
    """Sales type filter for real estate charts"""

    class Meta:
        db_table = 'real_estate_sale_filter'

    chart = ForeignKeyField(
        RealEstateChart, db_column='chart',
        related_name='_sale_filter')
    kauf = BooleanField(null=True, default=None)
    miete_pacht = BooleanField(null=True, default=None)
    erbpacht = BooleanField(null=True, default=None)
    leasing = BooleanField(null=True, default=None)

    def approve(self, real_estate):
        """Approves the given real estate against the sales type filter"""
        if self.kauf is not None and self.kauf != real_estate.kauf:
            return False

        if self.miete_pacht is not None:
            if self.miete_pacht != real_estate.miete_pacht:
                return False

        if self.erbpacht is not None and self.erbpacht != real_estate.erbpacht:
            return False

        if self.leasing is not None and self.leasing != real_estate.leasing:
            return False

        return True


class RealEstateAttributes(DSCMS4Model):
    """Real estate attributes to be
    shown within the respective chart
    """

    class Meta:
        db_table = 'real_estate_attributes'

    chart = ForeignKeyField(RealEstateChart, db_column='chart')
    attribute = CharField(255)


class FacebookChart(Chart):
    """Facebook data chart"""

    class Meta:
        db_table = 'facebook_chart'

    days = SmallIntegerField(default=14)
    limit = SmallIntegerField(default=10)
    facebook_id = CharField(255)
    facebook_name = CharField(255)


class ImageTextChart(Chart):
    """A chart that may contain images"""

    class Meta:
        db_table = 'image_text_chart'

    random = BooleanField(default=False)
    loop_limit = SmallIntegerField()
    scale = BooleanField(default=False)
    fullscreen = BooleanField(default=False)
    ken_burns = BooleanField(default=False)


class ScheduledChartImage(DSCMS4Model):
    """Scheduled images for charts"""

    class Meta:
        db_table = 'scheduled_chart_image'

    chart = ForeignKeyField(ImageTextChart, db_column='chart')
    file = IntegerField(db_column='image')
    image = FileProperty(file)
    schedule = ForeignKeyField(Schedule, db_column='schedule')


class ScheduledChartText(DSCMS4Model):
    """Scheduled text for charts"""

    class Meta:
        db_table = 'scheduled_chart_text'

    chart = ForeignKeyField(ImageTextChart, db_column='chart')
    text = TextField()
    schedule = ForeignKeyField(Schedule, db_column='schedule')


class VideoChart(Chart):
    """A chart that may contain images and texts"""

    class Meta:
        db_table = 'video_chart'

    file = IntegerField()
    video = FileProperty(file)
    schedule = ForeignKeyField(Schedule, db_column='schedule')
