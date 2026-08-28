"""Read operations for Port Statistics.

OLH topics: olhPortStatistics, olhSuspendedInterfaces
"""
from tasks import ArubaSwitch


def get_port_statistics(sw: ArubaSwitch):
    """Return list of dicts with port statistics.

    OLH: olhPortStatistics
    """
    sw.navigate('switching', 'port_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-port-statistics').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_suspended_interfaces(sw: ArubaSwitch):
    """Return list of dicts with suspended interfaces.

    OLH: olhSuspendedInterfaces
    """
    sw.navigate('switching', 'port_config')
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
                                status: cells[1].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)
