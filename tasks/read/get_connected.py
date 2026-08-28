"""Read operations for Network/Connected configuration.

OLH topics: olhIPv4, olhNetworkSetup
"""
from tasks import ArubaSwitch


def get_ipv4_setup(sw: ArubaSwitch):
    """Return dict with IPv4 setup.

    OLH: olhIPv4
    """
    sw.navigate('setup', 'get_connected')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('IP Address')) {
                    if (i + 1 < lines.length) {
                        result.ip_address = lines[i + 1];
                    }
                }
                if (line.includes('Subnet Mask')) {
                    if (i + 1 < lines.length) {
                        result.subnet_mask = lines[i + 1];
                    }
                }
                if (line.includes('Gateway')) {
                    if (i + 1 < lines.length) {
                        result.gateway = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_network_setup(sw: ArubaSwitch):
    """Return dict with network setup.

    OLH: olhNetworkSetup
    """
    sw.navigate('setup', 'get_connected')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('DNS')) {
                    if (i + 1 < lines.length) {
                        result.dns = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
