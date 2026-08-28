"""Read operations for IGMP Snooping configuration.

OLH topics: olhIGMPSnooping, olhIGMPSnoopingGlobal, olhIGMPForwarding,
            olhIGMPMulticast, olhIGMPVLANSettings
"""
from tasks import ArubaSwitch


def get_igmp_snooping_status(sw: ArubaSwitch):
    """Return dict with IGMP snooping global status.

    OLH: olhIGMPSnooping
    """
    sw.navigate('switching', 'igmp_snooping')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_igmp_forwarding(sw: ArubaSwitch):
    """Return dict with IGMP forwarding status.

    OLH: olhIGMPForwarding
    """
    sw.navigate('switching', 'igmp_snooping')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def list_igmp_multicast(sw: ArubaSwitch):
    """Return list of dicts with IGMP multicast entries.

    OLH: olhIGMPMulticast
    """
    sw.navigate('switching', 'igmp_snooping')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Group Address') || headers.includes('Multicast')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 2) {
                            result.push({
                                group_address: cells[0].innerText.trim(),
                                vlan: cells[1].innerText.trim(),
                                ports: cells.length > 2 ? cells[2].innerText.trim() : ''
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def get_igmp_per_vlan(sw: ArubaSwitch):
    """Return list of dicts with IGMP snooping per VLAN.

    OLH: olhIGMPVLANSettings
    """
    sw.navigate('switching', 'igmp_snooping')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('VLAN')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 2) {
                            result.push({
                                vlan: cells[0].innerText.trim(),
                                enabled: cells[1].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)
