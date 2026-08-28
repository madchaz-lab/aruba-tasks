"""Read operations for Routing configuration and statistics.

OLH topics: olhRouting, olhRoutingConfiguration, olhRouteTable, olhStaticRoutes,
            olhRoutingStatistics
"""
from tasks import ArubaSwitch


def get_routing_global(sw: ArubaSwitch):
    """Return dict with routing global settings.

    OLH: olhRouting
    """
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def list_route_table(sw: ArubaSwitch):
    """Return list of dicts with route table entries.

    OLH: olhRouteTable
    """
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Destination') || headers.includes('Network')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 3) {
                            result.push({
                                destination: cells[0].innerText.trim(),
                                gateway: cells[1].innerText.trim(),
                                interface: cells[2].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def list_static_routes(sw: ArubaSwitch):
    """Return list of dicts with static route configuration.

    OLH: olhStaticRoutes
    """
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-static-route').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_routing_stats(sw: ArubaSwitch):
    """Return dict with routing statistics.

    OLH: olhRoutingStatistics
    """
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Routes')) {
                    if (i + 1 < lines.length) {
                        result.routes = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
