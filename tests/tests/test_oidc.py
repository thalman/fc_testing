from __future__ import annotations

import pytest
from lib.roles.httpd import Httpd
from lib.roles.keycloak import Keycloak
from lib.topology import KnownTopology

import requests
import inspect
import time

CA = "/etc/pki/ca-trust/source/anchors/FederationComponentsTesting.crt"


@pytest.mark.topology(KnownTopology.FC)
def test_http_get_ca(httpd: Httpd, keycloak: Keycloak):
    """
    Check that web is running.

    This test is here just to identify that the
    containers are deployed and reachable
    """
    r = requests.get(f"https://{httpd.host.hostname}/public/", verify=CA)
    assert r.status_code >= 200 and r.status_code < 300, "Apache httpd web server is not reachable. Test environment is broken."


@pytest.mark.topology(KnownTopology.FC)
def test_http_get_keycloack(httpd: Httpd, keycloak: Keycloak):
    """
    Check that keycloak is running.

    This test is here just to identify that the
    containers are deployed and reachable
    """
    r = requests.get(f"https://{keycloak.host.hostname}:8443/", verify=CA)
    assert r.status_code >= 200 and r.status_code < 499, "Keycloack server is not reachable. Test environment is broken."


@pytest.mark.topology(KnownTopology.FC)
def test_new_cve(httpd: Httpd, keycloak: Keycloak):
    """
    Check segfault on empty post.

    steps:
    - set config with OIDCPreservePost On
    - restart httpd
    - post request without any data

    expected result:
    - apache httpd continues running
    - child process did not die either
    """
    cfg = """
        LoadModule authz_core_module modules/mod_authz_core.so
        LoadModule unixd_module modules/mod_unixd.so
        LoadModule cgi_module modules/mod_cgi.so
        LoadModule authn_core_module modules/mod_authn_core.so
        LoadModule authz_user_module modules/mod_authz_user.so
        LoadModule auth_openidc_module modules/mod_auth_openidc.so
        OIDCMetadataDir /tmp
        OIDCRedirectURI /sso_redirect
        OIDCCryptoPassphrase "exec:/usr/bin/openssl rand -base64 20"
        OIDCPreservePost On
        <Location /private >
            AuthType openid-connect
            Require valid-user
        </Location>
    """
    httpd.fs.write("/etc/httpd/conf.d/oidc.conf", inspect.cleandoc(cfg))
    httpd.prepare_httpd()
    try:
        r = requests.post(f"https://{httpd.host.hostname}/private/", verify=CA)
        assert r.status_code != 0
    except Exception:
        assert False, "Exception while performing POST request without data"
    time.sleep(1)
    status = httpd.host.conn.run("supervisorctl status httpd")
    assert "RUNNING" in status.stdout, "Apache httpd is not running any more"

    log = httpd.fs.read("/var/log/httpd/error_log")
    assert not ("segmentation fault" in log.lower()), "Apache httpd child process segfault"
