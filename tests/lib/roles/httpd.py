"""Apache httpd web multihost role."""

from __future__ import annotations

from pytest_mh import MultihostRole
from pytest_mh.utils.fs import LinuxFileSystem

from ..hosts.httpd import HttpdHost

class Httpd(MultihostRole[HttpdHost]):
    """
    Apache httpd server role.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fs: LinuxFileSystem = LinuxFileSystem(self.host)

    def prepare_httpd(self) -> None:
        self.host.conn.run("supervisorctl stop httpd")
        self.host.conn.run("rm -f /var/log/httpd/*")
        self.host.conn.run("supervisorctl start httpd")
