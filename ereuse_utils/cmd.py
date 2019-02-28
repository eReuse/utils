import subprocess
from contextlib import suppress
from typing import Any, TextIO

from ereuse_utils import text


def run(*cmd: Any,
        out=subprocess.PIPE,
        err=subprocess.DEVNULL,
        to_string=True,
        check=True,
        **kwargs) -> subprocess.CompletedProcess:
    """subprocess.run with a better API.

    :param cmd: A list of commands to execute as parameters.
                Parameters will be passed-in to ``str()`` so they
                can be any object that can handle str().
    :param out: As ``subprocess.run.stdout``.
    :param err: As ``subprocess.run.stderr``.
    :param to_string: As ``subprocess.run.universal_newlines``.
    :param check: As ``subprocess.run.check``.
    :param kwargs: Any other parameters that ``subprocess.run``
                   accepts.
    :return: The result of executing ``subprocess.run``.
    """
    return subprocess.run(tuple(str(c) for c in cmd),
                          stdout=out,
                          stderr=err,
                          universal_newlines=to_string,
                          check=check,
                          **kwargs)


class ProgressiveCmd:
    """Executes a cmd while interpreting its completion percentage.

    The completion percentage of the cmd is stored in
    :attr:`.percentage` and the user can obtain percentage
    increments by executing :meth:`.increment`.

    This class is useful to use within a child thread, so a main
    thread can request from time to time the percentage / increment
    status of the running command.
    """
    READ_LINE = None
    DECIMALS = 5
    INT = 3

    def __init__(self, *cmd: Any,
                 stdout=subprocess.DEVNULL,
                 number_chars: int = INT,
                 read: int = READ_LINE,
                 callback=None):
        """
        :param cmd: The command to execute.
        :param stderr: the stderr passed-in to Popen.
        :param stdout: the stdout passed-in to Popen
        :param number_chars: The number of chars used to represent
                             the percentage. Normalized cases are
                             :attr:`.DECIMALS` and :attr:`.INT`.
        :param read: For commands that do not print lines, how many
                     characters we should read between updates.
                     The percentage should be between those
                     characters.
        :param callback: If passed in, this method is executed every time
                         run gets an update from the command, passing
                         in the increment from the last execution.
                         If not passed-in, you can get such increment
                         by executing manually the ``increment`` method.
        """
        self.cmd = tuple(str(c) for c in cmd)
        self.read = read
        self.step = 0
        self.number_chars = number_chars
        # We call subprocess in the main thread so the main thread
        # can react on ``CalledProcessError`` exceptions
        self.conn = conn = subprocess.Popen(self.cmd,
                                            universal_newlines=True,
                                            stderr=subprocess.PIPE,
                                            stdout=stdout)
        self.out = conn.stdout if stdout == subprocess.PIPE else conn.stderr  # type: TextIO
        self._callback = callback
        self.last_update_percentage = 0
        self.percentage = 0

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, v):
        self._percentage = v
        if self._callback and self._percentage > 0:
            self._callback(self.increment())

    def run(self) -> None:
        """Processes the output."""
        while True:
            out = self.out.read(self.read) if self.read else self.out.readline()
            if out:
                with suppress(IndexError):
                    self.percentage = tuple(text.positive_percentages(out))[-1]
            else:  # No more output
                break
        if self.conn.wait() == 1:  # wait until cmd ends
            raise subprocess.CalledProcessError(self.conn.returncode,
                                                self.conn.args,
                                                stderr=self.conn.stderr.read())
        self.percentage = 100  # some cmds do not output 100 when completed

    def increment(self):
        """Returns the increment of progression from
        the last time this method is executed.
        """
        # for cmd badblocks the increment can be negative at the
        # beginning of the second step where last_percentage
        # is 100 and percentage is 0. By using max we
        # kind-of reset the increment and start counting for
        # the second step
        increment = max(self.percentage - self.last_update_percentage, 0)
        self.last_update_percentage = self.percentage
        return increment
