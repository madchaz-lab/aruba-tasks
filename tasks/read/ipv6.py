"""Read operations for IPv6 configuration.

OLH topics: olhIPv6
"""
from tasks import ArubaSwitch


def get_ipv6_setup(sw: ArubaSwitch):
    """Return dict with IPv6 setup.

    OLH: olhIPv6
    """
    sw.navigate('setup', 'get_connected')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('IPv6');
            return result;
        }
    """)
