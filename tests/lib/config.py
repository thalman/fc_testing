from __future__ import annotations

from typing import Type

from pytest_mh import MultihostConfig, MultihostDomain, MultihostHost, MultihostRole


class FCMultihostConfig(MultihostConfig):
    @property
    def id_to_domain_class(self) -> dict[str, Type[MultihostDomain]]:
        """
        Map domain id to domain class. Asterisk ``*`` can be used as fallback
        value.

        :rtype: Class name.
        """
        return {"*": FCMultihostDomain}


class FCMultihostDomain(MultihostDomain[FCMultihostConfig]):
    @property
    def role_to_host_class(self) -> dict[str, Type[MultihostHost]]:
        """
        Map role to host class. Asterisk ``*`` can be used as fallback value.

        :rtype: Class name.
        """
        from .hosts.keycloak import KeycloakHost
        from .hosts.httpd import HttpdHost

        return {
            "keycloak": KeycloakHost,
            "httpd": HttpdHost,
        }

    @property
    def role_to_role_class(self) -> dict[str, Type[MultihostRole]]:
        """
        Map role to role class. Asterisk ``*`` can be used as fallback value.

        :rtype: Class name.
        """
        from .roles.keycloak import Keycloak
        from .roles.httpd import Httpd

        return {
            "keycloak": Keycloak,
            "httpd": Httpd,
        }
