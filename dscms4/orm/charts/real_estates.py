"""Real estate chart ORM."""

from collections import defaultdict
from enum import Enum
from itertools import chain

from peewee import BooleanField, SmallIntegerField, IntegerField, \
    ForeignKeyField, CharField

from openimmodb import Immobilie
from peeweeplus import JSONField, EnumField

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

    display_format = JSONField(
        EnumField, DisplayFormat, default=DisplayFormat.BIG_PICTURE,
        key='displayFormat')
    ken_burns = JSONField(BooleanField, default=False, key='kenBurns')
    scaling = JSONField(BooleanField, default=False, key='scaling')
    slideshow = JSONField(BooleanField, default=True, key='slideshow')
    qr_codes = JSONField(BooleanField, default=False, key='qrCodes')
    show_contact = JSONField(BooleanField, default=True, key='showContact')
    contact_picture = JSONField(
        BooleanField, default=True, key='contactPicture')
    font_size = JSONField(SmallIntegerField, default=8, key='fontSize')
    font_color = JSONField(IntegerField, default=0x000000, key='fontColor')
    # Data field selections:
    amenities = JSONField(BooleanField, default=True)
    construction = JSONField(BooleanField, default=True)
    courtage = JSONField(BooleanField, default=True)
    floor = JSONField(BooleanField, default=True)
    area = JSONField(BooleanField, default=True)
    free_from = JSONField(BooleanField, default=True, key='freeFrom')
    coop_share = JSONField(BooleanField, default=True, key='coopShare')
    total_area = JSONField(BooleanField, default=True, key='totalArea')
    plot_area = JSONField(BooleanField, default=True, key='plotArea')
    cold_rent = JSONField(BooleanField, default=True, key='coldRent')
    purchase_price = JSONField(BooleanField, default=True, key='purchasePrice')
    security_deposit = JSONField(
        BooleanField, default=True, key='securityDeposit')
    service_charge = JSONField(BooleanField, default=True, key='serviceCharge')
    object_id = JSONField(BooleanField, default=True, key='objectId')
    description = JSONField(BooleanField, default=True)
    warm_rent = JSONField(BooleanField, default=True, key='warmRent')
    rooms = JSONField(BooleanField, default=True)
    # Amenities tags:
    lift = JSONField(BooleanField, default=True)
    bathtub = JSONField(BooleanField, default=True)
    balcony = JSONField(BooleanField, default=True)
    accessibility = JSONField(BooleanField, default=True)
    assited_living = JSONField(
        BooleanField, default=True, key='assistedLiving')
    carport = JSONField(BooleanField, default=True)
    floorboards = JSONField(BooleanField, default=True)
    duplex = JSONField(BooleanField, default=True)
    shower = JSONField(BooleanField, default=True)
    builtin_kitchen = JSONField(
        BooleanField, default=True, key='builtinKitchen')
    screed = JSONField(BooleanField, default=True)  # Estrich.
    tiles = JSONField(BooleanField, default=True)
    outdoor_parking = JSONField(
        BooleanField, default=True, key='outdoorParking')
    garage = JSONField(BooleanField, default=True)
    cable_sat_tv = JSONField(BooleanField, default=True, key='cableSatTv')
    fireplace = JSONField(BooleanField, default=True)
    basement = JSONField(BooleanField, default=True)
    plastic = JSONField(BooleanField, default=True)
    furnished = JSONField(BooleanField, default=True)
    parquet = JSONField(BooleanField, default=True)
    car_park = JSONField(BooleanField, default=True, key='carPark')
    wheelchair_accessible = JSONField(
        BooleanField, default=True, key='wheelchairAccessible')
    sauna = JSONField(BooleanField, default=True)
    stone = JSONField(BooleanField, default=True)
    swimming_pool = JSONField(BooleanField, default=True, key='swimmingPool')
    carpet = JSONField(BooleanField, default=True)
    underground_carpark = JSONField(
        BooleanField, default=True, key='undergroundCarpark')
    lavatory = JSONField(BooleanField, default=True)
    # Rooms selector:
    rooms_1 = JSONField(BooleanField, default=True, key='rooms1')
    rooms_2 = JSONField(BooleanField, default=True, key='rooms2')
    rooms_3 = JSONField(BooleanField, default=True, key='rooms3')
    rooms_4 = JSONField(BooleanField, default=True, key='rooms4')
    rooms_5 = JSONField(BooleanField, default=True, key='rooms5')
    rooms_5_or_more = JSONField(BooleanField, default=True, key='rooms5orMore')
    # Real estate type:
    finance_project = JSONField(
        BooleanField, default=True, key='financeProject')
    business_realty = JSONField(
        BooleanField, default=True, key='businessRealty')
    short_term_accommodation = JSONField(
        BooleanField, default=True, key='shortTermAccomodation')
    living_realty = JSONField(BooleanField, default=True, key='livingRealty')
    # Subtypes:
    office = JSONField(BooleanField, default=True)
    retail = JSONField(BooleanField, default=True)
    recreational = JSONField(BooleanField, default=True)
    hospitality_industry = JSONField(
        BooleanField, default=True, key='hospitalityIndustry')
    plot = JSONField(BooleanField, default=True)
    hall_warehouse_production = JSONField(
        BooleanField, default=True, key='hallWarehouseProduction')
    house = JSONField(BooleanField, default=True)
    agriculture_forestry = JSONField(
        BooleanField, default=True, key='agricultureForestry')
    miscellaneous = JSONField(BooleanField, default=True)
    flat = JSONField(BooleanField, default=True)
    room = JSONField(BooleanField, default=True)
    income_property = JSONField(
        BooleanField, default=True, key='incomeProperty')
    # Sale type:
    emphyteusis = JSONField(BooleanField, default=True)     # Erbpacht.
    leasing = JSONField(BooleanField, default=True)
    rent = JSONField(BooleanField, default=True)
    sale = JSONField(BooleanField, default=True)

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

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        xml = super().to_dom(dom.RealEstates)
        xml.display_format = self.display_format.value
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

    chart = JSONField(
        ForeignKeyField, RealEstates, column_name='chart',
        backref='id_filters', on_delete='CASCADE')
    value = JSONField(CharField, 255)
    type_ = JSONField(EnumField, IdTypes, column_name='type')

    def __call__(self, real_estate):
        """Checks the filter against the respective real estate."""
        if self.typ == IdTypes.INTERN:
            return self.value == real_estate.objektnr_intern

        if self.typ == IdTypes.EXTERN:
            return self.value == real_estate.objektnr_extern

        if self.typ == IdTypes.OPENIMMO:
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
        xml.type = self.type_.value
        return xml


class ZipCodeFilter(DSCMS4Model):
    """Filter for real estate ZIP codes."""

    class Meta:
        table_name = 'filter_zip_code'

    chart = JSONField(
        ForeignKeyField, RealEstates, column_name='chart',
        backref='zip_code_filters', on_delete='CASCADE')
    zip_code = JSONField(CharField, 255, key='zipCode')
    # True: blacklist, False: whitelist.
    blacklist = JSONField(BooleanField, default=False)

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
