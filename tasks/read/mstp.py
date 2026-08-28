"""Read operations for MSTP (Multiple Spanning Tree Protocol) configuration.

OLH topics: olhMSTP, olhMSTPConfiguration, olhMSTPInterface
"""
from tasks import ArubaSwitch


def get_mstp_config(sw: ArubaSwitch):
    """Return dict with MSTP global configuration.

    OLH: olhMSTP
    """
    sw.navigate('spanning_tree', 'mstp_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_mstp_per_port(sw: ArubaSwitch):
    """Return list of dicts with MSTP per port configuration.

    OLH: olhMSTPInterface
    """
    sw.navigate('spanning_tree', 'mstp_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Interface')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 2) {
                            result.push({
                                interface: cells[0].innerText.trim(),
                                port_role: cells[1].innerText.trim(),
                                forwarding_state: cells.length > 2 ? cells[2].innerText.trim() : ''
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)
