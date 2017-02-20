"""Object Relational Mappings"""

from datetime import datetime
from peewee import MySQLDatabase, PrimaryKeyField, ForeignKeyField, \
    CharField, TextField, DateTimeField

from homeinfo.peewee import Model


class ComCatModel(Model):
    """Basic ORM model for ComCat"""

    class Meta:
        database = database
        schema = database.database

    id = PrimaryKeyField()


class OrganizationUnit(ComCatModel):
    """An organizational unit"""

    customer = ForeignKeyField(Customer, db_column='customer')
    parent = ForeignKeyField('self', db_column='parent')
    name = CharField(255)
    annotation = CharField(255, null=True, default=None)


class Chart(ComCatModel):
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
