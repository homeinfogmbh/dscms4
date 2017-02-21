"""Object Relational Mappings"""

from datetime import datetime
from peewee import ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from filedb import FileProperty

from .common import DSCMS4Model


class NoWhitelist(Exception):
    """Indicates that no white list is available"""

    pass


class NoBlacklist(Exception):
    """Indicates that no black list is available"""

    pass


class Schedule(DSCMS4Model):
    """Date / time schedule

    Weekdays are a binary integer:
        Mon | Tue | Wed | Thu | Fri | Sat | Sun
        2^6   2^5   2^4   2^3   2^2   2^1   2^0
    """

    STR_TEMP = ('Begin: {begin}\n'
                'End:   {end}\n'
                '\n'
                'Mon │ Tue │ Wed │ Thu │ Fri │ Sat │ Sun\n'
                '────┼─────┼─────┼─────┼─────┼─────┼────\n'
                ' {}  │  {}  │  {}  │  {}  │  {}  │  {}  │  {}\n')

    begin = DateTimeField(null=True)
    end = DateTimeField(null=True)
    weekdays = SmallIntegerField(default=127)

    def __str__(self):
        days = ['✓' if match else '✗' for match in (
            self.match_day(day) for day in range(7))]
        return self.STR_TEMP.format(*days, begin=self.begin, end=self.end)

    @property
    def monday(self):
        """Determines whether the schedule runs on mondays"""
        return self.match_day(0)

    @monday.setter
    def monday(self, value):
        """Sets monday to the respective value"""
        self.set_day(0, value)

    @property
    def tuesday(self):
        """Determines whether the schedule runs on tuesdays"""
        return self.match_day(1)

    @tuesday.setter
    def tuesday(self, value):
        """Sets tuesday to the respective value"""
        self.set_day(1, value)

    @property
    def wednesday(self):
        """Determines whether the schedule runs on wednesdays"""
        return self.match_day(2)

    @wednesday.setter
    def wednesday(self, value):
        """Sets wednesday to the respective value"""
        self.set_day(2, value)

    @property
    def thursday(self):
        """Determines whether the schedule runs on thursdays"""
        return self.match_day(3)

    @thursday.setter
    def thursday(self, value):
        """Sets thursday to the respective value"""
        self.set_day(3, value)

    @property
    def friday(self):
        """Determines whether the schedule runs on fridays"""
        return self.match_day(4)

    @friday.setter
    def friday(self, value):
        """Sets friday to the respective value"""
        self.set_day(4, value)

    @property
    def saturday(self):
        """Determines whether the schedule runs on saturdays"""
        return self.match_day(5)

    @saturday.setter
    def saturday(self, value):
        """Sets saturday to the respective value"""
        self.set_day(5, value)

    @property
    def sunday(self):
        """Determines whether the schedule runs on sundays"""
        return self.match_day(6)

    @sunday.setter
    def sunday(self, value):
        """Sets sunday to the respective value"""
        self.set_day(6, value)

    @property
    def all_week(self):
        """Determines whether the schedule runs all week"""
        return self.weekdays == 0b1111111

    @property
    def active(self):
        """Determines whether the schedule is currently active"""
        return self.matches(datetime.now())

    def match_day(self, day):
        """Determines whether the schedule
        runs on the respective day
        """
        return self.all_week or self.weekdays & (1 << 6 - day)

    def set_day(self, day, value):
        """Set the respective day"""
        mask = 1 << 6 - day
        self.weekdays &= ~mask

        if value:
            self.weekdays |= mask

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
