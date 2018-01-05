"""Group messages."""

__all__ = [
    'NoSuchGroup',
    'NoSuchMemberType',
    'NoSuchMember',
    'GroupAdded',
    'GroupPatched',
    'GroupDeleted',
    'MemberAdded',
    'MemberDeleted']


class NoSuchGroup(DSCMS4Message):
    """Indicates that the respective group does not exist."""

    STATUS = 404


class NoSuchMemberType(DSCMS4Message):
    """Indicates that the respective member type does not exist."""

    STATUS = 404


class NoSuchMember(DSCMS4Message):
    """Indicates that the respective member does not exist."""

    STATUS = 404


class GroupAdded(DSCMS4Message):
    """Indicates that the group was successfully added."""

    STATUS = 201


class GroupPatched(DSCMS4Message):
    """Indicates that the group was successfully patched."""

    STATUS = 200


class GroupDeleted(DSCMS4Message):
    """Indicates that the group was successfully deleted."""

    STATUS = 200


class MemberAdded(DSCMS4Message):
    """Indicates that the group member was successfully added."""

    STATUS = 201


class MemberDeleted(DSCMS4Message):
    """Indicates that the group member was successfully deleted."""

    STATUS = 200
