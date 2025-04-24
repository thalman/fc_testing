from __future__ import annotations

from enum import unique
from typing import final

from pytest_mh import KnownTopologyBase, Topology, TopologyDomain, TopologyMark


@final
@unique
class KnownTopology(KnownTopologyBase):
    """
    Well-known topologies that can be given to ``pytest.mark.topology``
    directly. It is expected to use these values in favor of providing
    custom marker values.

    .. code-block:: python
        :caption: Example usage

        @pytest.mark.topology(KnownTopology.FC)
        def test_something(httpd: Httpd, keycloak: Keycloak):
            assert True
    """

    FC = TopologyMark(
        name="fc",
        topology=Topology(TopologyDomain("fc", httpd=1, keycloak=1)),
        fixtures=dict(httpd="fc.httpd[0]", keycloak="fc.keycloak[0]"),
    )
