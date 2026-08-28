"""Read operations for Loop Protection configuration.

OLH topics: olhLoopProtection, olhLoopProtectionGlobal, olhLoopProtectionInterface
"""
from tasks import ArubaSwitch


def get_loop_protection_status(sw: ArubaSwitch):
    """Return dict with Loop Protection global status.

    OLH: olhLoopProtection
    """
    sw.navigate('security', 'loop_protection')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_loop_protection_per_interface(sw: ArubaSwitch):
    """Return list of dicts with Loop Protection per interface.

    OLH: olhLoopProtectionInterface
    """
    sw.navigate('security', 'loop_protection')
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
