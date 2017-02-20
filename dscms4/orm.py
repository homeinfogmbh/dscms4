"""Object Relational Mappings"""

from datetime import datetime
from peewee import MySQLDatabase, PrimaryKeyField, ForeignKeyField, \
    CharField, TextField, DateTimeField, BooleanField, SmallIntegerField

from homeinfo.peewee import Model


class DSCMS4Model(Model):
    """Basic ORM model for ComCat"""

    class Meta:
        database = database
        schema = database.database

    id = PrimaryKeyField()


class OrganizationUnit(DSCMS4Model):
    """An organizational unit"""

    customer = ForeignKeyField(Customer, db_column='customer')
    parent = ForeignKeyField('self', db_column='parent')
    name = CharField(255)
    annotation = CharField(255, null=True, default=None)


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


# ### Real estate filters ### #
class RealEstateZIPWhitelist(DSCMS4Model):
    """ZIP code white list for real estate charts"""

    class Meta:
        db_table = 'real_estate_zip_whitelist'

    chart = ForeignKeyField(RealEstateChart, db_column='chart')
    zip_code = CharField(255)


class RealEstateZIPBlacklist(RealEstateZIPWhitelist):
    """ZIP code black list for real estate charts"""

    class Meta:
        db_table = 'real_estate_zip_blacklist'


class RealEstateUsageFilter(DSCMS4Model):
    """Usage type selector list for real estate charts"""

    class Meta:
        db_table = 'real_estate_usage_filter'

    chart = ForeignKeyField(RealEstateChart, db_column='chart')
    wohnen = BooleanField(null=True, default=None)
    gewerbe = BooleanField(null=True, default=None)
    anlage = BooleanField(null=True, default=None)
    waz = BooleanField(null=True, default=None)


    def approve(self, real_estate):
        """Approve openimmodb.Immobilie real estate ORM model"""
        if self.wohnen is not None and self.wohnen != real_estate.wohnen:
            return False

        if self.gewerbe is not None and self.gewerbe != real_estate.gewerbe:
            return False

        if self.anlage is not None and self.anlage != real_estate.anlage:
            return False

        if self.waz is not None and self.waz != real_estate.waz:
            return False

        return True


class RealEstateTypeFilter(DSCMS4Model):
    """Real estate type filter for real estate charts"""

    class Meta:
        db_table = 'real_estate_type_filter'

    chart = ForeignKeyField(RealEstateChart, db_column='chart')
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

    # TODO: implement
