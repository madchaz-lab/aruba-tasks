"""Read operations for EEE (Energy Efficient Ethernet) configuration.

OLH topics: olhEEE, olhEEEGlobal, olhEEEInterface
"""
from tasks import ArubaSwitch


def get_eee_global_status(sw: ArubaSwitch):
    """Return dict with EEE global status.

    OLH: olhEEE
    """
    sw.navigate('switching', 'eee_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_eee_per_interface(sw: ArubaSwitch):
    """Return list of dicts with EEE per interface settings.

    OLH: olhEEEInterface
    """
    sw.navigate('switching', 'eee_config')
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
