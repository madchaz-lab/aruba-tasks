"""Read operations for CST (Common Spanning Tree) configuration.

OLH topics: olhCST, olhCSTConfiguration
"""
from tasks import ArubaSwitch


def get_cst_status(sw: ArubaSwitch):
    """Return dict with CST global status.

    OLH: olhCST
    """
    sw.navigate('spanning_tree', 'cst_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = {};
            const body = document.body.innerText;

            // Check if CST is enabled
            result.enabled = body.includes('Enabled');

            return result;
        }
    """)


def get_cst_config(sw: ArubaSwitch):
    """Return list of dicts with CST port configuration.

    OLH: olhCSTConfiguration
    Table: table with Interface/Port Role/Port Forwarding State headers
    """
    sw.navigate('spanning_tree', 'cst_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Port Role')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 6) {
                            result.push({
                                interface: cells[1].innerText.trim(),
                                port_role: cells[2].innerText.trim(),
                                port_forwarding_state: cells[3].innerText.trim(),
                                port_priority: cells[4].innerText.trim(),
                                port_path_cost: cells[5].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)
