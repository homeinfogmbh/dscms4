"""Real estate chart ORM."""

from collections import defaultdict
from enum import Enum

from peewee import BooleanField, SmallIntegerField, IntegerField, \
    ForeignKeyField, CharField

from openimmodb import Immobilie
from peeweeplus import EnumField

from dscms4 import dom
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.charts.common import Chart

__all__ = ['RealEstates', 'IdFilter', 'ZipCodeFilter']


class DisplayFormat(Enum):
    """Display formats."""

    BIG_PICTURE = 'big picture'
    THREE = 'three'
    FIFTY_FIFTY = 'fifty-fifty'


class IdTypes(Enum):
    """Real estate ID types."""

    INTERN = 'objektnr_intern'
    EXTERN = 'objektnr_extern'
    OPENIMMO = 'openimmo_obid'


class RealEstates(Chart):
    """Chart for real estate displaying."""

    class Meta:
        table_name = 'chart_real_estates'

    display_format = EnumField(
        DisplayFormat, default=DisplayFormat.BIG_PICTURE)
    ken_burns = BooleanField(default=False)
    scaling = BooleanField(default=False)
    slideshow = BooleanField(default=True)
    qr_codes = BooleanField(default=False)
    show_contact = BooleanField(default=True)
    contact_picture = BooleanField(default=True)
    font_size = SmallIntegerField(default=8)
    font_color = IntegerField(default=0x000000)
    # Data field selections:
    amenities = BooleanField(default=True)
    construction = BooleanField(default=True)
    courtage = BooleanField(default=True)
    floor = BooleanField(default=True)
    area = BooleanField(default=True)
    free_from = BooleanField(default=True)
    coop_share = BooleanField(default=True)
    total_area = BooleanField(default=True)
    plot_area = BooleanField(default=True)
    cold_rent = BooleanField(default=True)
    purchase_price = BooleanField(default=True)
    security_deposit = BooleanField(default=True)
    service_charge = BooleanField(default=True)
    object_id = BooleanField(default=True)
    description = BooleanField(default=True)
    warm_rent = BooleanField(default=True)
    rooms = BooleanField(default=True)
    # Amenities tags:
    lift = BooleanField(default=True)
    bathtub = BooleanField(default=True)
    balcony = BooleanField(default=True)
    accessibility = BooleanField(default=True)
    assited_living = BooleanField(default=True)
    carport = BooleanField(default=True)
    floorboards = BooleanField(default=True)
    duplex = BooleanField(default=True)
    shower = BooleanField(default=True)
    builtin_kitchen = BooleanField(default=True)
    screed = BooleanField(default=True)     # Estrich.
    tiles = BooleanField(default=True)
    outdoor_parking = BooleanField(default=True)
    garage = BooleanField(default=True)
    cable_sat_tv = BooleanField(default=True)
    fireplace = BooleanField(default=True)
    basement = BooleanField(default=True)
    plastic = BooleanField(default=True)
    furnished = BooleanField(default=True)
    parquet = BooleanField(default=True)
    car_park = BooleanField(default=True)
    wheelchair_accessible = BooleanField(default=True)
    sauna = BooleanField(default=True)
    stone = BooleanField(default=True)
    swimming_pool = BooleanField(default=True)
    carpet = BooleanField(default=True)
    underground_carpark = BooleanField(default=True)
    lavatory = BooleanField(default=True)
    # Rooms selector:
    rooms_1 = BooleanField(default=True)
    rooms_2 = BooleanField(default=True)
    rooms_3 = BooleanField(default=True)
    rooms_4 = BooleanField(default=True)
    rooms_5 = BooleanField(default=True)
    rooms_5_or_more = BooleanField(default=True)
    # Real estate type:
    finance_project = BooleanField(default=True)
    business_realty = BooleanField(default=True)
    short_term_accommocation = BooleanField(default=True)
    living_realty = BooleanField(default=True)
    # Subtypes:
    office = BooleanField(default=True)
    retail = BooleanField(default=True)
    recreational = BooleanField(default=True)
    hospitality_industry = BooleanField(default=True)
    plot = BooleanField(default=True)
    hall_warehouse_production = BooleanField(default=True)
    house = BooleanField(default=True)
    agriculture_forestry = BooleanField(default=True)
    miscellaneous = BooleanField(default=True)
    flat = BooleanField(default=True)
    room = BooleanField(default=True)
    income_property = BooleanField(default=True)
    # Sale type:
    emphyteusis = BooleanField(default=True)    # Erbpacht.
    leasing = BooleanField(default=True)
    rent = BooleanField(default=True)
    sale = BooleanField(default=True)

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
        """Creates a new chart from the respective dictionary."""
        filters = dictionary.pop('filters', {})
        base, chart = super().from_dict(customer, dictionary, **kwargs)
        yield base
        yield chart

        for id_filter in filters.get('id', ()):
            yield IdFilter.from_dict(chart, id_filter)

        for zip_code_filter in filters.get('zip_code', ()):
            yield ZipCodeFilter.from_dict(chart, zip_code_filter)

    @property
    def zip_code_whitelist(self):
        """Yields ZIP code whitelist filters."""
        return ZipCodeFilter.select().where(
            (ZipCodeFilter.chart == self) & (ZipCodeFilter.blacklist == 0))

    @property
    def zip_code_blacklist(self):
        """Yields ZIP code blacklist filters."""
        return ZipCodeFilter.select().where(
            (ZipCodeFilter.chart == self) & (ZipCodeFilter.blacklist == 1))

    @property
    def real_estates(self):
        """Yields filtered real estates for this chart."""
        return self.filter(Immobilie.select().where(
            Immobilie.customer == self.customer))

    @property
    def filters_dictionary(self):
        """Dictionary of filters."""
        filters = defaultdict(list)

        for fltr in IdFilter.select().where(IdFilter.chart == self):
            filters['id'].append(fltr.to_dict())

        for fltr in ZipCodeFilter.select().where(ZipCodeFilter.chart == self):
            filters['zip_code'].append(fltr.to_dict())

        return filters

    def match(self, real_estate):
        """Matches the respective real estate
        against the configures filters.
        """
        # Discard blacklisted real estates.
        if any(fltr(real_estate) for fltr in self.zip_code_blacklist):
            return False

        zip_code_whitelist = tuple(self.zip_code_whitelist)

        if zip_code_whitelist:
            # Discard non-whitelisted real estates
            # iff ZIP code whitelist has entries.
            if not any(fltr(real_estate) for fltr in zip_code_whitelist):
                return False

        id_filters = tuple(self.id_filters)

        if id_filters:
            # Discard non-whitelisted real estates
            # iff ID whitelist has entries.
            if not any(fltr(real_estate) for fltr in id_filters):
                return False

        return True

    def filter(self, real_estates):
        """Yields filtered real estates."""
        return filter(self.match_real_estate, real_estates)

    def to_dict(self):
        """Returns a JSON-ish dictionary of the record's properties."""
        dictionary = super().to_dict()
        dictionary['filters'] = self.filters_dictionary
        return dictionary

    def to_dom(self):
        """Returns an XML DOM of this chart."""
        xml = super().to_dom(dom.RealEstates)
        xml.display_format = self.display_format
        xml.ken_burns = self.ken_burns
        xml.scaling = self.scaling
        xml.slideshow = self.slideshow
        xml.qr_codes = self.qr_codes
        xml.show_contact = self.show_contact
        xml.contact_picture = self.contact_picture
        xml.font_size = self.font_size
        xml.font_color = self.font_color
        # Data field selections:
        xml.amenities = self.amenities
        xml.construction = self.construction
        xml.courtage = self.courtage
        xml.floor = self.floor
        xml.area = self.area
        xml.free_from = self.free_from
        xml.coop_share = self.coop_share
        xml.total_area = self.total_area
        xml.plot_area = self.plot_area
        xml.cold_rent = self.cold_rent
        xml.purchase_price = self.purchase_price
        xml.security_deposit = self.security_deposit
        xml.service_charge = self.service_charge
        xml.object_id = self.object_id
        xml.description = self.description
        xml.warm_rent = self.warm_rent
        xml.rooms = self.rooms
        # Amenities tags:
        xml.lift = self.lift
        xml.bathtub = self.bathtub
        xml.balcony = self.balcony
        xml.accessibility = self.accessibility
        xml.assited_living = self.assited_living
        xml.carport = self.carport
        xml.floorboards = self.floorboards
        xml.duplex = self.duplex
        xml.shower = self.shower
        xml.builtin_kitchen = self.builtin_kitchen
        xml.screed = self.screed
        xml.tiles = self.tiles
        xml.outdoor_parking = self.outdoor_parking
        xml.garage = self.garage
        xml.cable_sat_tv = self.cable_sat_tv
        xml.fireplace = self.fireplace
        xml.basement = self.basement
        xml.plastic = self.plastic
        xml.furnished = self.furnished
        xml.parquet = self.parquet
        xml.car_park = self.car_park
        xml.wheelchair_accessible = self.wheelchair_accessible
        xml.sauna = self.sauna
        xml.stone = self.stone
        xml.swimming_pool = self.swimming_pool
        xml.carpet = self.carpet
        xml.underground_carpark = self.underground_carpark
        xml.lavatory = self.lavatory
        # Rooms selector:
        xml.rooms_1 = self.rooms_1
        xml.rooms_2 = self.rooms_2
        xml.rooms_3 = self.rooms_3
        xml.rooms_4 = self.rooms_4
        xml.rooms_5 = self.rooms_5
        xml.rooms_5_or_more = self.rooms_5_or_more
        # Real estate type:
        xml.finance_project = self.finance_project
        xml.business_realty = self.business_realty
        xml.short_term_accommocation = self.short_term_accommocation
        xml.living_realty = self.living_realty
        # Subtypes:
        xml.office = self.office
        xml.retail = self.retail
        xml.recreational = self.recreational
        xml.hospitality_industry = self.hospitality_industry
        xml.plot = self.plot
        xml.hall_warehouse_production = self.hall_warehouse_production
        xml.house = self.house
        xml.agriculture_forestry = self.agriculture_forestry
        xml.miscellaneous = self.miscellaneous
        xml.flat = self.flat
        xml.room = self.room
        xml.income_property = self.income_property
        # Sale type:
        xml.emphyteusis = self.emphyteusis
        xml.leasing = self.leasing
        xml.rent = self.rent
        xml.sale = self.sale
        xml.filter = [
            filter.to_dom() for filter in chain(
                self.id_filters, self.zip_code_filters)]
        return xml


class IdFilter(DSCMS4Model):
    """Filter for the object IDs."""

    class Meta:
        table_name = 'filter_id'

    chart = ForeignKeyField(
        RealEstates, column_name='chart', backref='id_filters',
        on_delete='CASCADE')
    value = CharField(255)
    type_ = EnumField(IdTypes, column_name='type')

    def __call__(self, real_estate):
        """Checks the filter against the respective real estate."""
        if self.typ == IdTypes.INTERN:
            return self.value == real_estate.objektnr_intern
        elif self.typ == IdTypes.EXTERN:
            return self.value == real_estate.objektnr_extern
        elif self.typ == IdTypes.OPENIMMO:
            return self.value == real_estate.openimmo_obid

        raise ValueError('Unexpected ID type.')

    @classmethod
    def from_dict(cls, chart, dictionary):
        """Creates a new entry from the
        dictionary for the respective chart.
        """
        record = super().from_dict(dictionary)
        record.chart = chart
        return record

    def to_dom(self):
        """Returns an XML DOM of this model."""
        xml = dom.IdFilter()
        xml.value_ = self.value
        xml.type = self.type
        return xml


class ZipCodeFilter(DSCMS4Model):
    """Filter for real estate ZIP codes."""

    class Meta:
        table_name = 'filter_zip_code'

    chart = ForeignKeyField(
        RealEstates, column_name='chart', backref='zip_code_filters',
        on_delete='CASCADE')
    zip_code = CharField(255)
    # True: blacklist, False: whitelist.
    blacklist = BooleanField(default=False)

    def __call__(self, real_estate):
        """Checks the filter against the respective real estate."""
        if self.blacklist:
            return real_estate.plz != self.zip_code

        return real_estate.plz == self.zip_code

    @classmethod
    def from_dict(cls, chart, dictionary):
        """Creates a new record from the respective dictionary."""
        record = super().from_dict(dictionary)
        record.chart = chart
        return record

    @property
    def whitelist(self):
        """Determines whether this is a whitelist record."""
        return not self.blacklist

    @whitelist.setter
    def whitelist(self, whitelist):
        """Sets whether this is a whitelist record."""
        self.blacklist = not whitelist

    def to_dom(self):
        """Returns an XML DOM of this model."""
        xml = dom.ZipCodeFilter()
        xml.zip_code = self.zip_code
        xml.blacklist = self.blacklist
        return xml
