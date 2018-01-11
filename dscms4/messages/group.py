"""Group messages."""

from his.messages import locales, Message

__all__ = [
    'NoSuchGroup',
    'NoSuchMemberType',
    'NoSuchMember',
    'GroupAdded',
    'GroupPatched',
    'GroupDeleted',
    'MemberAdded',
    'MemberDeleted']


class GroupMessage(Message):
    """Base class for content related messages."""

    LOCALES = locales('/etc/dscms4.d/locales/group.ini')


class NoSuchGroup(GroupMessage):
    """Indicates that the respective group does not exist."""

    STATUS = 404


class NoSuchMemberType(GroupMessage):
    """Indicates that the respective member type does not exist."""

    STATUS = 404


class NoSuchMember(GroupMessage):
    """Indicates that the respective member does not exist."""

    STATUS = 404


class GroupAdded(GroupMessage):
    """Indicates that the group was successfully added."""

    STATUS = 201


class GroupPatched(GroupMessage):
    """Indicates that the group was successfully patched."""

    STATUS = 200


class GroupDeleted(GroupMessage):
    """Indicates that the group was successfully deleted."""

    STATUS = 200


class MemberAdded(GroupMessage):
    """Indicates that the group member was successfully added."""

    STATUS = 201


class MemberDeleted(GroupMessage):
    """Indicates that the group member was successfully deleted."""

    STATUS = 200
