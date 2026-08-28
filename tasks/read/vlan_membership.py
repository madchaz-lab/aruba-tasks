"""Read operations for VLAN Membership.

OLH topics: olhVLANMembership
"""
from tasks import ArubaSwitch


def list_vlan_membership_by_interface(sw: ArubaSwitch):
    """Return list of dicts with VLAN membership by interface.

    OLH: olhVLANMembership
    """
    sw.navigate('vlan', 'vlan_config')
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
                                vlan: cells[1].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def list_vlan_membership_by_vlan(sw: ArubaSwitch):
    """Return list of dicts with VLAN membership by VLAN.

    OLH: olhVLANMembership
    """
    sw.navigate('vlan', 'vlan_config')
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
                                members: cells[1].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)
