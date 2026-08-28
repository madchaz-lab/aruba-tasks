"""Read operations for Class of Service configuration.

OLH topics: olhCoS, olhCoSDSCP, olhCoSPriority, olhCoSQueue,
            olhCoSShaping, olhCoSStatistics, olhCoSGeneral
"""
from tasks import ArubaSwitch


def get_cos_general_settings(sw: ArubaSwitch):
    """Return dict with general CoS settings (trust mode).

    OLH: olhCoS, olhCoSGeneral
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = {};
            const body = document.body.innerText;
            const idx = body.indexOf('Trust Mode');
            if (idx >= 0) {
                const after = body.substring(idx + 10).trim();
                const lines = after.split('\\n');
                if (lines.length > 0) {
                    result.trust_mode = lines[0];
                }
            }
            return result;
        }
    """)


def list_interface_cos_config(sw: ArubaSwitch):
    """Return list of dicts with per-interface CoS configuration.

    OLH: olhCoSShaping
    Table: first table with Interface/Default 802.1p Priority/Shaping Rate headers
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Default 802.1p Priority')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 3) {
                            result.push({
                                interface: cells[1].innerText.trim(),
                                default_p_priority: cells[2].innerText.trim(),
                                shaping_rate: cells[3].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def list_cos_statistics(sw: ArubaSwitch):
    """Return list of dicts with queue statistics per interface.

    OLH: olhCoSStatistics
    Table: table with Interface/Queue/Transmitted Packets/Tail Dropped Packets headers
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Transmitted Packets')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 7) {
                            result.push({
                                interface: cells[1].innerText.trim(),
                                queue: cells[2].innerText.trim(),
                                tx_packets: cells[3].innerText.trim(),
                                tail_dropped_packets: cells[4].innerText.trim(),
                                tx_bytes: cells[5].innerText.trim(),
                                tail_dropped_bytes: cells[6].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def list_priority_map(sw: ArubaSwitch):
    """Return list of dicts with 802.1p priority to traffic class mapping.

    OLH: olhCoSPriority
    Note: This data is in a flat section, not a DataTable. Parsing from body text.
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const body = document.body.innerText;
            const idx = body.indexOf('802.1p Priority Mapping');
            if (idx < 0) return result;

            const after = body.substring(idx + 23).trim();
            const lines = after.split('\\n').map(l => l.trim()).filter(l => l);

            // Skip header lines
            let i = 0;
            while (i < lines.length && (lines[i] === '802.1p Priority' || lines[i] === 'Traffic Class')) {
                i++;
            }

            // Parse pairs
            while (i < lines.length) {
                if (lines[i] === 'Queue Configuration' || lines[i] === 'DSCP CoS Mapping') break;
                if (i + 1 < lines.length) {
                    result.push({
                        priority: lines[i],
                        traffic_class: lines[i + 1]
                    });
                    i += 2;
                } else {
                    i++;
                }
            }
            return result;
        }
    """)


def list_queue_config(sw: ArubaSwitch):
    """Return list of dicts with queue configuration (scheduler type, WRR weight, etc).

    OLH: olhCoSQueue
    Note: This data is in a flat section, not a DataTable. Parsing from body text.
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const body = document.body.innerText;
            const idx = body.indexOf('Queue Configuration');
            if (idx < 0) return result;

            const after = body.substring(idx + 19).trim();
            const lines = after.split('\\n').map(l => l.trim()).filter(l => l);

            // Skip header lines
            let i = 0;
            while (i < lines.length && (lines[i] === 'Queue' || lines[i] === 'Scheduler Type' ||
                   lines[i] === 'WRR Weight (1 - 255)' || lines[i] === 'WRR Percentage')) {
                i++;
            }

            // Parse rows: queue, scheduler_type, wrr_weight, wrr_percentage
            while (i < lines.length) {
                if (lines[i] === 'DSCP CoS Mapping') break;
                if (i + 3 < lines.length) {
                    result.push({
                        queue: lines[i],
                        scheduler_type: lines[i + 1],
                        wrr_weight: lines[i + 2],
                        wrr_percentage: lines[i + 3]
                    });
                    i += 4;
                } else {
                    i++;
                }
            }
            return result;
        }
    """)


def list_dscp_cos_map(sw: ArubaSwitch):
    """Return list of dicts with DSCP to CoS mapping.

    OLH: olhCoSDSCP
    Note: This data is in a flat section, not a DataTable. Parsing from body text.
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const body = document.body.innerText;
            const idx = body.indexOf('DSCP CoS Mapping');
            if (idx < 0) return result;

            const after = body.substring(idx + 16).trim();
            const lines = after.split('\\n').map(l => l.trim()).filter(l => l);

            // Skip header lines
            let i = 0;
            while (i < lines.length && (lines[i] === 'IP DSCP' || lines[i] === 'Traffic Class')) {
                i++;
            }

            // Parse pairs
            while (i < lines.length) {
                if (lines[i] === 'Interface CoS Configuration') break;
                if (i + 1 < lines.length) {
                    result.push({
                        dscp: lines[i],
                        traffic_class: lines[i + 1]
                    });
                    i += 2;
                } else {
                    i++;
                }
            }
            return result;
        }
    """)
