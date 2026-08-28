"""Read operations for MAC table configuration.

OLH topics: olhMACAddressTable, olhMACAddressTableGlobal, olhMACAddressTableInterface
"""
from tasks import ArubaSwitch


def list_mac_table(sw: ArubaSwitch):
    """Return list of dicts with MAC address table entries.

    OLH: olhMACAddressTable
    Table: #datagrid-mac-adress (note: typo in Aruba's ID)
    """
    sw.navigate('diagnostics', 'mac_table')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-mac-adress').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_mac_table_global(sw: ArubaSwitch):
    """Return dict with MAC table global settings.

    OLH: olhMACAddressTableGlobal
    """
    sw.navigate('diagnostics', 'mac_table')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Max Entries')) {
                    if (i + 1 < lines.length) {
                        result.max_entries = lines[i + 1];
                    }
                }
                if (line.includes('Aging Time')) {
                    if (i + 1 < lines.length) {
                        result.aging_time = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
