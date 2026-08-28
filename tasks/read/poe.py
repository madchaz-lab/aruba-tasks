"""Read operations for POE configuration.

OLH topics: olhPOE, olhPOEPorts, olhPOESchedule, olhPOEConsumptionHistory
"""
from tasks import ArubaSwitch


def list_poe_ports(sw: ArubaSwitch):
    """Return list of dicts with POE port configuration.

    OLH: olhPOE
    """
    sw.navigate('switching', 'port_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('POE') || headers.includes('Power')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 2) {
                            result.push({
                                interface: cells[0].innerText.trim(),
                                power: cells[1].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def get_poe_schedule(sw: ArubaSwitch):
    """Return dict with POE schedule configuration.

    OLH: olhPOESchedule
    """
    sw.navigate('setup', 'schedule_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_poe_consumption_history(sw: ArubaSwitch):
    """Return dict with POE consumption history.

    OLH: olhPOEConsumptionHistory
    """
    sw.navigate('switching', 'port_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Consumption')) {
                    if (i + 1 < lines.length) {
                        result.consumption = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
