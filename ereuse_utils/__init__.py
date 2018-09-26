import json
import locale
from collections import Iterable
from datetime import datetime, timedelta
from decimal import Decimal
from distutils.version import StrictVersion
from typing import Generator
from uuid import UUID


class JSONEncoder(json.JSONEncoder):
    """An overloaded JSON Encoder with extra type support."""

    def default(self, obj):
        if hasattr(obj, 'value'):  # an enumerated value
            return obj.value
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            return round(obj.total_seconds())
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, StrictVersion):
            return str(obj)
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, Dumpeable):
            return obj.dump()
        return json.JSONEncoder.default(self, obj)  # do not do ``super``


class Dumpeable:
    """Dumps dictionaries and jsons for Devicehub.

    A base class to allow subclasses to generate dictionaries
    and json suitable for sending to a Devicehub, i.e. preventing
    private and  constants to be in the JSON and camelCases field names.
    """

    ENCODER = JSONEncoder

    def dump(self):
        """
        Creates a dictionary consisting of the
        non-private fields of this instance with camelCase field names.
        """
        d = vars(self).copy()
        for name in vars(self).keys():
            if name.startswith('_') or name[0].isupper():
                del d[name]
            else:
                import inflection
                d[inflection.camelize(name, uppercase_first_letter=False)] = d.pop(name)
        return d

    def to_json(self):
        """
        Creates a JSON representation of the non-private fields of
        this class.
        """
        return json.dumps(self, cls=self.ENCODER, indent=2)


def ensure_utf8(app_name_to_show_on_error: str):
    """
    Python3 uses by default the system set, but it expects it to be
    ‘utf-8’ to work correctly.
    This can generate problems in reading and writing files and in
    ``.decode()`` method.

    An example how to 'fix' it::

        echo 'export LC_CTYPE=en_US.UTF-8' > .bash_profile
        echo 'export LC_ALL=en_US.UTF-8' > .bash_profile
    """
    encoding = locale.getpreferredencoding()
    if encoding.lower() != 'utf-8':
        raise OSError(
            '{} works only in UTF-8, but yours is set at {}'
            ''.format(app_name_to_show_on_error, encoding))


def now() -> datetime:
    """
    Returns a compatible 'now' with DeviceHub's API,
    this is as UTC and without microseconds.
    """
    return datetime.utcnow().replace(microsecond=0)


def flatten_mixed(values: Iterable) -> Generator:
    """
    Flatten a list containing lists and other elements. This is not deep.

    >>> list(flatten_mixed([1, 2, [3, 4]]))
    [1, 2, 3, 4]
    """
    for x in values:
        if isinstance(x, list):
            for y in x:
                yield y
        else:
            yield x
