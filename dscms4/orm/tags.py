"""Entity tags."""

from peewee import ForeignKeyField, CharField

from .common import CustomerModel

__all__ = [
    'find',
    'find_all',
    'find_and_count',
    'find_with_matches',
    'find_top',
    'TerminalTag',
    'ComCatAccountTag',
    'ApartmentBuildingTag']


def find(tag):
    """Finds entities by tags."""

    for terminal_tag in TerminalTag.select().where(TerminalTag.tag == tag):
        yield terminal_tag.terminal

    for comcat_account_tag in ComCatAccountTag.select().where(
            ComCatAccountTag.tag == tag):
        yield comcat_account_tag.comcat_account

    for apartment_building_tag in ApartmentBuildingTag.select().where(
            ApartmentBuildingTag.tag == tag):
        yield apartment_building_tag.apartment_building


def find_all(tags):
    """Finds all matching entities for the provided tags."""

    for tag in tags:
        for entity in find(tag):
            yield entity


def find_and_count(tags):
    """Finds and counts matches of entities."""

    occurences = defaultdict(int)

    for entity in find_all(tags):
        occurences[entity] += 1

    return occurences


def find_with_matches(tags):
    """Yields tuple of amount of matches
    and entity for each matched entity.
    """

    for entity, matches in find_matches(tags).items():
        yield (matches, entity)


def find_top(tags):
    """Finds and sorts matching entities."""

    for _, entity in sorted(find_with_matches(tags), reverse=True):
        yield entity


class Tag(CustomerModel):
    """A basic, abstract tag."""

    tag = CharField(255)

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        return {'id': self.id, 'customer': self.customer.id}


class TerminalTag(Tag):
    """Tags for terminals."""

    class Meta:
        db_table = 'tags_terminal'

    terminal = ForeignKeyField(Terminal, db_column='terminal')

    @classmethod
    def from_list(cls, customer, terminal, lst):
        """Creates tags for the customer
        and terminal from the respective list.
        """
        for tag in lst:
            record = cls()
            record.customer = customer
            record.terminal = terminal
            record.tag = tag
            yield record

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict()
        dictionary['terminal'] = self.terminal.id
        return dictionary


class ComCatAccountTag(Tag):
    """Tags for ComCat accounts."""

    class Meta:
        db_table = 'tags_comcat_account'

    comcat_account = ForeignKeyField(ComCatAccount, db_column='comcat_account')

    @classmethod
    def from_list(cls, customer, comcat_account, lst):
        """Creates tags for the customer
        and terminal from the respective list.
        """
        for tag in lst:
            record = cls()
            record.customer = customer
            record.comcat_account = comcat_account
            record.tag = tag
            yield record

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict()
        dictionary['comcat_account'] = self.comcat_account.id
        return dictionary


class ApartmentBuildingTag(Tag):
    """Tags for apartment buildings."""

    class Meta:
        db_table = 'tags_apartment_building'

    apartment_building = ForeignKeyField(
        ApartmentBuilding, db_column='apartment_building')

    @classmethod
    def from_list(cls, customer, apartment_building, lst):
        """Creates tags for the customer
        and terminal from the respective list.
        """
        for tag in lst:
            record = cls()
            record.customer = customer
            record.apartment_building = apartment_building
            record.tag = tag
            yield record

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict()
        dictionary['apartment_building'] = self.apartment_building.id
        return dictionary