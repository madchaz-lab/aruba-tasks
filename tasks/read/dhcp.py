"""Read operations for DHCP configuration.

OLH topics: olhDHCPRelay, olhDHCPRelayGlobal, olhDHCPRelayInterfaces,
            olhDHCPRelayServer, olhDHCPSnooping, olhDHCPSnoopingGlobal,
            olhDHCPVLANSettings, olhDHCPInterfaceSettings, olhDHCPBindingDatabase
"""
from tasks import ArubaSwitch


def list_dhcp_relay_servers(sw: ArubaSwitch):
    """Return list of dicts with DHCP relay server configuration.

    OLH: olhDHCPRelayServer
    Table: #datagrid-dhcp-server-conf
    """
    sw.navigate('routing', 'dhcp_relay')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-dhcp-server-conf').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_dhcp_relay_interfaces(sw: ArubaSwitch):
    """Return list of dicts with DHCP relay interface configuration.

    OLH: olhDHCPRelayInterfaces
    Table: #datagrid-dhcp-interface
    """
    sw.navigate('routing', 'dhcp_relay')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-dhcp-interface').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_dhcp_snooping_status(sw: ArubaSwitch):
    """Return dict with DHCP snooping global status.

    OLH: olhDHCPSnooping, olhDHCPSnoopingGlobal
    """
    sw.navigate('security', 'dhcp_snooping')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = {};
            const body = document.body.innerText;

            // Check if DHCP snooping is enabled
            result.enabled = body.includes('Enabled');

            return result;
        }
    """)


def list_dhcp_bindings(sw: ArubaSwitch):
    """Return list of dicts with DHCP binding database entries.

    OLH: olhDHCPBindingDatabase
    Note: This may require navigation to a different page or tab.
    """
    sw.navigate('routing', 'dhcp_relay')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('IPAddress') || headers.includes('MACAddress')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 2) {
                            result.push({
                                ip_address: cells[0].innerText.trim(),
                                mac_address: cells[1].innerText.trim(),
                                vlan: cells.length > 2 ? cells[2].innerText.trim() : ''
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)
