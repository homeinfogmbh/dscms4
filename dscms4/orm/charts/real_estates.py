"""Real estate chart ORM."""

from collections import defaultdict
from enum import Enum

from peewee import Model, BooleanField, SmallIntegerField, IntegerField, \
    ForeignKeyField, CharField

from openimmodb import Immobilie
from peeweeplus import EnumField

from dscms4.orm.common import DSCMS4Model
from dscms4.orm.charts.common import Chart


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


class RealEstates(Model, Chart):
    """Chart for real estate displaying."""

    class Meta:
        db_table = 'chart_real_estates'

    display_format = EnumField(DisplayFormat)
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
    uderground_carpark = BooleanField(default=True)
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
    def from_dict(cls, dictionary):
        """Creates a new chart from the respective dictionary."""
        chart = super().from_dict(dictionary)
        chart.display_format = dictionary.get('display_format')
        chart.ken_burns = dictionary.get('ken_burns')
        chart.scaling = dictionary.get('scaling')
        chart.slideshow = dictionary.get('slideshow')
        chart.qr_codes = dictionary.get('qr_codes')
        chart.show_contact = dictionary.get('show_contact')
        chart.contact_picture = dictionary.get('contact_picture')
        chart.font_size = dictionary.get('font_size')
        chart.font_color = dictionary.get('font_color')
        # Data field selections:
        chart.amenities = dictionary.get('amenities')
        chart.construction = dictionary.get('construction')
        chart.courtage = dictionary.get('courtage')
        chart.floor = dictionary.get('floor')
        chart.area = dictionary.get('area')
        chart.free_from = dictionary.get('free_from')
        chart.coop_share = dictionary.get('coop_share')
        chart.total_area = dictionary.get('total_area')
        chart.plot_area = dictionary.get('plot_area')
        chart.cold_rent = dictionary.get('cold_rent')
        chart.purchase_price = dictionary.get('purchase_price')
        chart.security_deposit = dictionary.get('security_deposit')
        chart.service_charge = dictionary.get('service_charge')
        chart.object_id = dictionary.get('object_id')
        chart.description = dictionary.get('description')
        chart.warm_rent = dictionary.get('warm_rent')
        chart.rooms = dictionary.get('rooms')
        # Amenities tags:
        chart.lift = dictionary.get('lift')
        chart.bathtub = dictionary.get('bathtub')
        chart.balcony = dictionary.get('balcony')
        chart.accessibility = dictionary.get('accessibility')
        chart.assited_living = dictionary.get('assited_living')
        chart.carport = BooleanField(default=True)
        chart.floorboards = BooleanField(default=True)
        chart.duplex = BooleanField(default=True)
        chart.shower = BooleanField(default=True)
        chart.builtin_kitchen = BooleanField(default=True)
        chart.screed = BooleanField(default=True)     # Estrich.
        chart.tiles = BooleanField(default=True)
        chart.outdoor_parking = BooleanField(default=True)
        chart.garage = BooleanField(default=True)
        chart.cable_sat_tv = BooleanField(default=True)
        chart.fireplace = BooleanField(default=True)
        chart.basement = BooleanField(default=True)
        chart.plastic = BooleanField(default=True)
        chart.furnished = BooleanField(default=True)
        chart.parquet = BooleanField(default=True)
        chart.car_park = BooleanField(default=True)
        chart.wheelchair_accessible = BooleanField(default=True)
        chart.sauna = BooleanField(default=True)
        chart.stone = BooleanField(default=True)
        chart.swimming_pool = BooleanField(default=True)
        chart.carpet = BooleanField(default=True)
        chart.uderground_carpark = BooleanField(default=True)
        chart.lavatory = BooleanField(default=True)
        # Rooms selector:
        chart.rooms_1 = BooleanField(default=True)
        chart.rooms_2 = BooleanField(default=True)
        chart.rooms_3 = BooleanField(default=True)
        chart.rooms_4 = BooleanField(default=True)
        chart.rooms_5 = BooleanField(default=True)
        chart.rooms_5_or_more = BooleanField(default=True)
        # Real estate type:
        chart.finance_project = BooleanField(default=True)
        chart.business_realty = BooleanField(default=True)
        chart.short_term_accommocation = BooleanField(default=True)
        chart.living_realty = BooleanField(default=True)
        # Subtypes:
        chart.office = BooleanField(default=True)
        chart.retail = BooleanField(default=True)
        chart.recreational = BooleanField(default=True)
        chart.hospitality_industry = BooleanField(default=True)
        chart.plot = BooleanField(default=True)
        chart.hall_warehouse_production = BooleanField(default=True)
        chart.house = BooleanField(default=True)
        chart.agriculture_forestry = BooleanField(default=True)
        chart.miscellaneous = BooleanField(default=True)
        chart.flat = BooleanField(default=True)
        chart.room = BooleanField(default=True)
        chart.income_property = BooleanField(default=True)
        # Sale type:
        chart.emphyteusis = BooleanField(default=True)    # Erbpacht.
        chart.leasing = BooleanField(default=True)
        chart.rent = BooleanField(default=True)
        chart.sale = BooleanField(default=True)
        yield chart
        filters = dictionary.get('filters', {})

        for id_filter in filters.get('id', ()):
            yield IdFilter.from_dict(id_filter, chart=chart)

        for zip_code_filter in filters.get('zip_code', ()):
            yield ZipCodeFilter.from_dict(zip_code_filter, chart=chart)

    @property
    def id_filters(self):
        """Yields ID filters of this chart."""
        return IdFilter.select().where(IdFilter.chart == self)

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
        return self.filter_real_estates(Immobilie.select().where(
            Immobilie.customer == self.customer))

    @property
    def dictionary(self):
        """Returns a JSON-ish dictionary of the record's properties."""
        return {
            'display_format': self.display_format,
            'ken_burns': self.ken_burns,
            'scaling': self.scaling,
            'slideshow': self.slideshow,
            'qr_codes': self.qr_codes,
            'show_contact': self.show_contact,
            'contact_picture': self.contact_picture,
            'font_size': self.font_size,
            'font_color': self.font_color,
            # Data field selections:
            'amenities': self.amenities,
            'construction': self.construction,
            'courtage': self.courtage,
            'floor': self.floor,
            'area': self.area,
            'free_from': self.free_from,
            'coop_share': self.coop_share,
            'total_area': self.total_area,
            'plot_area': self.plot_area,
            'cold_rent': self.cold_rent,
            'purchase_price': self.purchase_price,
            'security_deposit': self.security_deposit,
            'service_charge': self.service_charge,
            'object_id': self.object_id,
            'description': self.description,
            'warm_rent': self.warm_rent,
            'rooms': self.rooms,
            # Amenities tags:
            'lift': self.lift,
            'bathtub': self.bathtub,
            'balcony': self.balcony,
            'accessibility': self.accessibility,
            'assited_living': self.assited_living,
            'carport': self.carport,
            'floorboards': self.floorboards,
            'duplex': self.duplex,
            'shower': self.shower,
            'builtin_kitchen': self.builtin_kitchen,
            'screed': self.screed,     # Estrich.
            'tiles': self.tiles,
            'outdoor_parking': self.outdoor_parking,
            'garage': self.garage,
            'cable_sat_tv': self.cable_sat_tv,
            'fireplace': self.fireplace,
            'basement': self.basement,
            'plastic': self.plastic,
            'furnished': self.furnished,
            'parquet': self.parquet,
            'car_park': self.car_park,
            'wheelchair_accessible': self.wheelchair_accessible,
            'sauna': self.sauna,
            'stone': self.stone,
            'swimming_pool': self.swimming_pool,
            'carpet': self.carpet,
            'uderground_carpark': self.uderground_carpark,
            'lavatory': self.lavatory,
            # Rooms selector:
            'rooms_1': self.rooms_1,
            'rooms_2': self.rooms_2,
            'rooms_3': self.rooms_3,
            'rooms_4': self.rooms_4,
            'rooms_5': self.rooms_5,
            'rooms_5_or_more': self.rooms_5_or_more,
            # Real estate type:
            'finance_project': self.finance_project,
            'business_realty': self.business_realty,
            'short_term_accommocation': self.short_term_accommocation,
            'living_realty': self.living_realty,
            # Subtypes:
            'office': self.office,
            'retail': self.retail,
            'recreational': self.recreational,
            'hospitality_industry': self.hospitality_industry,
            'plot': self.plot,
            'hall_warehouse_production': self.hall_warehouse_production,
            'house': self.house,
            'agriculture_forestry': self.agriculture_forestry,
            'miscellaneous': self.miscellaneous,
            'flat': self.flat,
            'room': self.room,
            'income_property': self.income_property,
            # Sale type:
            'emphyteusis': self.emphyteusis,
            'leasing': self.leasing,
            'rent': self.rent,
            'sale': self.sale}

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict()
        dictionary.update(self.dictionary)
        dictionary['filters'] = defaultdict(list)

        for id_filter in IdFilter.select().where(IdFilter.chart == self):
            dictionary['filters']['id'].append(id_filter.to_dict())

        for zip_code_filter in ZipCodeFilter.select().where(
                ZipCodeFilter.chart == self):
            dictionary['filters']['zip_code'].append(zip_code_filter.to_dict())

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
            # Discard non-whitelisted real estates#
            # iff ID whitelist has entries.
            if not any(fltr(real_estate) for fltr in id_filters):
                return False

        return True

    def filter_real_estates(self, real_estates):
        """Yields filtered real estates."""
        return filter(self.match, real_estates)


class IdFilter(Model, DSCMS4Model):
    """Filter for the object IDs."""

    class Meta:
        db_table = 'filter_id'

    chart = ForeignKeyField(RealEstates, db_column='chart')
    value = CharField(255)
    typ = EnumField(IdTypes, db_column='types')

    def __call__(self, real_estate):
        """Checks the filter against the respective real estate."""
        if self.typ == IdTypes.INTERN:
            return self.value == real_estate.objektnr_intern
        elif self.typ == IdTypes.EXTERN:
            return self.value == real_estate.objektnr_extern
        elif self.typ == IdTypes.OPENIMMO:
            return self.value == real_estate.openimmo_obid
        else:
            raise ValueError('Unexpected ID type.')

    @classmethod
    def from_dict(cls, dictionary, chart=None):
        """Creates a new entry from the
        dictionary for the respective chart.
        """
        record = cls()
        record.chart = chart
        record.value = dictionary['value']
        record.typ = dictionary['type']
        return record

    def to_dict(self):
        """Converts the record into a JSON-ish dictionary."""
        return {'value': self.value, 'type': self.typ}


class ZipCodeFilter(Model, DSCMS4Model):
    """Filter for real estate ZIP codes."""

    class Meta:
        db_table = 'filter_zip_code'

    chart = ForeignKeyField(RealEstates, db_column='chart')
    zip_code = CharField(255)
    # True: blacklist, False: whitelist.
    blacklist = BooleanField(default=False)

    def __call__(self, real_estate):
        """Checks the filter against the respective real estate."""
        if self.blacklist:
            return real_estate.plz != self.zip_code

        return real_estate.plz == self.zip_code

    @classmethod
    def from_dict(cls, dictionary, chart=None):
        """Creates a new record from the respective dictionary."""
        record = cls()
        record.chart = chart
        record.zip_code = dictionary['zip_code']
        record.blacklist = dictionary.get('blacklist')
        return record

    @property
    def whitelist(self):
        """Determines whether this is a whitelist record."""
        return not self.blacklist

    @whitelist.setter
    def whitelist(self, whitelist):
        """Sets whether this is a whitelist record."""
        self.blacklist = not whitelist

    def to_dict(self):
        """Converts the record into a JSON-ish dictionary."""
        return {'zip_code': self.zip_code, 'blacklist': self.blacklist}
