"""Keycloak multihost role."""

from __future__ import annotations

from pytest_mh import MultihostRole
from pytest_mh.utils.fs import LinuxFileSystem

from ..hosts.keycloak import KeycloakHost

class Keycloak(MultihostRole[KeycloakHost]):
    """
    Keycloak role.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fs: LinuxFileSystem = LinuxFileSystem(self.host)
