from __future__ import annotations

from pytest_mh import MultihostHost

from ..config import FCMultihostDomain


class KeycloakHost(MultihostHost[FCMultihostDomain]):
    """
    Keycloak host object.

    Nothing special needed
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
