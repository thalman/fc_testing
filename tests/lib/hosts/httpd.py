from __future__ import annotations

from pytest_mh import MultihostHost

from ..config import FCMultihostDomain


class HttpdHost(MultihostHost[FCMultihostDomain]):
    """
    Httpd host object.

    Nothing special needed
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
