"""Read operations for DoS Protection configuration.

OLH topics: olhDoSProtection, olhDoSProtectionInterface, olhSYNAttackProtection,
            olhSYNFIN, olhSYNProtectionMode
"""
from tasks import ArubaSwitch


def get_dos_protection_status(sw: ArubaSwitch):
    """Return dict with DoS protection global settings.

    OLH: olhDoSProtection
    """
    sw.navigate('security', 'dos_protection')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            const result = {};

            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('DoS Protection')) {
                    if (i + 1 < lines.length) {
                        result.enabled = lines[i + 1].includes('Enabled');
                    }
                }
                if (line.includes('SYN Protection Mode')) {
                    if (i + 1 < lines.length) {
                        result.syn_mode = lines[i + 1];
                    }
                }
                if (line.includes('SYN Protection Threshold')) {
                    if (i + 1 < lines.length) {
                        result.syn_threshold = lines[i + 1];
                    }
                }
                if (line.includes('SYN Protection Period')) {
                    if (i + 1 < lines.length) {
                        result.syn_period = lines[i + 1];
                    }
                }
                if (line.includes('SYN Attack Status')) {
                    if (i + 1 < lines.length) {
                        result.syn_attack_status = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_dsp_per_interface(sw: ArubaSwitch):
    """Return list of dicts with DoS protection per interface.

    OLH: olhDoSProtectionInterface
    """
    sw.navigate('security', 'dos_protection')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Status')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 2) {
                            result.push({
                                interface: cells[0].innerText.trim(),
                                status: cells[1].innerText.trim(),
                                last_syn_attack: cells.length > 2 ? cells[2].innerText.trim() : ''
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def get_syn_attack_status(sw: ArubaSwitch):
    """Return list of dicts with SYN attack status per interface.

    OLH: olhSYNAttackProtection
    """
    sw.navigate('security', 'dos_protection')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Status')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 3) {
                            result.push({
                                interface: cells[0].innerText.trim(),
                                status: cells[1].innerText.trim(),
                                last_syn_attack: cells[2].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)
