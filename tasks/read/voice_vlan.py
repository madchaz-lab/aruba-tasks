"""Read operations for Voice VLAN configuration.

OLH topics: olhVoiceVLAN, olhVoiceVLANGlobal, olhVoiceVLANInterface, olhVoiceVLANOUI
"""
from tasks import ArubaSwitch


def get_voice_vlan_global(sw: ArubaSwitch):
    """Return dict with Voice VLAN global settings.

    OLH: olhVoiceVLAN
    """
    sw.navigate('vlan', 'voice_vlan')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_voice_vlan_per_interface(sw: ArubaSwitch):
    """Return list of dicts with Voice VLAN per interface settings.

    OLH: olhVoiceVLANInterface
    """
    sw.navigate('vlan', 'voice_vlan')
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


def list_voice_vlan_ouis(sw: ArubaSwitch):
    """Return list of dicts with Voice VLAN OUI entries.

    OLH: olhVoiceVLANOUI
    """
    sw.navigate('vlan', 'voice_vlan')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('OUI')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 2) {
                            result.push({
                                oui: cells[0].innerText.trim(),
                                vendor: cells[1].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)
