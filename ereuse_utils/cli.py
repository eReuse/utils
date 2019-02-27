import enum as _enum
import getpass
import itertools
import os
import pathlib
import threading
from contextlib import contextmanager
from time import sleep
from typing import Type

from boltons import urlutils
from click import types as click_types
from colorama import Fore
from tqdm import tqdm

from ereuse_utils import if_none_return_none

COMMON_CONTEXT_S = {'help_option_names': ('-h', '--help')}
"""Common Context settings used for our implementations of the 
Click cli.
"""


class Enum(click_types.Choice):
    """
    Enum support for click.

    Use it as a collection: @click.option(..., type=cli.Enum(MyEnum)).
    Then, this expects you to pass the *name* of a member of the enum.

    From `this github issue <https://github.com/pallets/click/issues/
    605#issuecomment-277539425>`_.
    """

    def __init__(self, enum: Type[_enum.Enum]):
        self.__enum = enum
        super().__init__(enum.__members__)

    def convert(self, value, param, ctx):
        return self.__enum[super().convert(value, param, ctx)]


class Path(click_types.Path):
    """Like click.Path but returning ``pathlib.Path`` objects."""

    def convert(self, value, param, ctx):
        return pathlib.Path(super().convert(value, param, ctx))


class URL(click_types.StringParamType):
    """Returns a bolton's URL."""

    name = 'url'

    def __init__(self,
                 scheme=None,
                 username=None,
                 password=None,
                 host=None,
                 port=None,
                 path=None,
                 query_params=None,
                 fragment=None) -> None:
        super().__init__()
        """Creates the type URL. You can require or enforce parts
        of the URL by setting parameters of this constructor.
        
        If the param is...
        
        - None, no check is performed (default).
        - True, it is then required as part of the URL.
        - False, it is then required NOT to be part of the URL.
        - Any other value, then such value is required to be in
          the URL.
        """
        self.attrs = (
            ('scheme', scheme),
            ('username', username),
            ('password', password),
            ('host', host),
            ('port', port),
            ('path', path),
            ('query_params', query_params),
            ('fragment', fragment)
        )

    @if_none_return_none
    def convert(self, value, param, ctx):
        url = urlutils.URL(super().convert(value, param, ctx))
        for name, attr in self.attrs:
            if attr is True:
                if not getattr(url, name):
                    self.fail('URL {} must contain {} but it does not.'.format(url, name))
            elif attr is False:
                if getattr(url, name):
                    self.fail('URL {} cannot contain {} but it does.'.format(url, name))
            elif attr:
                if getattr(url, name) != attr:
                    self.fail('{} form {} can only be {}'.format(name, url, attr))
        return url


def password(service: str, username: str, prompt: str = 'Password:') -> str:
    """Gets a password from the keyring or the terminal."""
    import keyring
    return keyring.get_password(service, username) or getpass.getpass(prompt)


class Line(tqdm):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self, iterable=None, desc=None, total=100, leave=True, file=None, ncols=None,
                 mininterval=0.2, maxinterval=10.0, miniters=None, ascii=None, disable=False,
                 unit='it', unit_scale=False, dynamic_ncols=False, smoothing=0.3,
                 bar_format=None,
                 initial=0, position=None, postfix=None, unit_divisor=1000, write_bytes=None,
                 gui=False, **kwargs):
        super().__init__(iterable, desc, total, leave, file, ncols, mininterval, maxinterval,
                         miniters, ascii, disable, unit, unit_scale, dynamic_ncols, smoothing,
                         bar_format, initial, position, postfix, unit_divisor, write_bytes, gui,
                         **kwargs)

    def write_at_line(self, *args):
        with self._lock:
            self.display(''.join(str(arg) for arg in args))

    @contextmanager
    def spin(self, prefix: str):
        self._stop_running = threading.Event()
        spin_thread = threading.Thread(target=self._spin, args=[prefix])
        spin_thread.start()
        try:
            yield
        finally:
            self._stop_running.set()
            spin_thread.join()

    def _spin(self, prefix: str):
        while not self._stop_running.is_set():
            self.write_at_line(prefix, next(self.spinner_cycle))
            sleep(0.50)

    @classmethod
    @contextmanager
    def reserve_lines(self, n):
        try:
            yield
        finally:
            self.move_down(n - 1)

    @classmethod
    def move_down(cls, n: int):
        print('\n' * n)


def clear():
    os.system('clear')


def title(text, ljust=38):
    return str(text).ljust(ljust)


def danger(text):
    return '{}{}'.format(Fore.RED, text)


def done():
    return '{}done.'.format(Fore.GREEN)
