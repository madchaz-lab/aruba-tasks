"""Read operations for LLDP configuration.

OLH topics: olhLLDP, olhLLDPGlobal, olhLLDPInterface, olhLLDPNeighbors, olhLLDPStats
"""
from tasks import ArubaSwitch


def get_lldp_global(sw: ArubaSwitch):
    """Return dict with LLDP global settings.

    OLH: olhLLDP
    """
    sw.navigate('neighbor_discovery', 'lldp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_lldp_per_interface(sw: ArubaSwitch):
    """Return list of dicts with LLDP per interface settings.

    OLH: olhLLDPInterface
    """
    sw.navigate('neighbor_discovery', 'lldp')
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
                                enabled: cells[1].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def list_lldp_neighbors(sw: ArubaSwitch):
    """Return list of dicts with LLDP neighbor information.

    OLH: olhLLDPNeighbors
    """
    sw.navigate('neighbor_discovery', 'lldp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Neighbor') || headers.includes('Device')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 3) {
                            result.push({
                                interface: cells[0].innerText.trim(),
                                neighbor: cells[1].innerText.trim(),
                                port: cells[2].innerText.trim(),
                                system_name: cells.length > 3 ? cells[3].innerText.trim() : ''
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def get_lldp_stats(sw: ArubaSwitch):
    """Return dict with LLDP statistics.

    OLH: olhLLDPStats
    """
    sw.navigate('neighbor_discovery', 'lldp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Tx frames')) {
                    if (i + 1 < lines.length) {
                        result.tx_frames = lines[i + 1];
                    }
                }
                if (line.includes('Rx frames')) {
                    if (i + 1 < lines.length) {
                        result.rx_frames = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
