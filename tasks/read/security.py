"""Read operations for Security configuration.

OLH topics: olhPortSecurity, olhPortAccessControl, olhProtectedPorts,
            olhPortAccessControlClient, olhPortAccessControlGlobal,
            olhPortAccessControlMac, olhPortAccessControlPort,
            olhPortAccessControlStatistics, olhPortAccessControlSupplicant,
            olhPortAccessControlVlan
"""
from tasks import ArubaSwitch


def list_port_security(sw: ArubaSwitch):
    """Return list of dicts with port security configuration.

    OLH: olhPortSecurity
    """
    sw.navigate('security', 'port_security')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-port-security').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_port_access_control(sw: ArubaSwitch):
    """Return list of dicts with port access control port configuration.

    OLH: olhPortAccessControl, olhPortAccessControlPort
    Table: #datagrid-port-configuration
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-port-configuration').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_port_access_control_global(sw: ArubaSwitch):
    """Return dict with port access control global settings.

    OLH: olhPortAccessControlGlobal
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def list_port_access_control_vlan(sw: ArubaSwitch):
    """Return list of dicts with port access control VLAN authentication.

    OLH: olhPortAccessControlVlan
    Table: #datagrid-vlan-authentication
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-vlan-authentication').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_port_access_control_supplicant(sw: ArubaSwitch):
    """Return list of dicts with supplicant credentials.

    OLH: olhPortAccessControlSupplicant
    Table: #datagrid-supplicant-credentials
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-supplicant-credentials').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_port_access_control_client(sw: ArubaSwitch):
    """Return list of dicts with client information.

    OLH: olhPortAccessControlClient
    Table: #datagrid-client-information
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-client-information').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_port_access_control_statistics(sw: ArubaSwitch):
    """Return list of dicts with port access control statistics.

    OLH: olhPortAccessControlStatistics
    Table: #datagrid-statistics
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-statistics').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_port_access_control_mac(sw: ArubaSwitch):
    """Return dict with MAC authentication settings.

    OLH: olhPortAccessControlMac
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('MAC Authentication')) {
                    if (i + 1 < lines.length) {
                        result.mac_auth = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def list_protected_ports(sw: ArubaSwitch):
    """Return list of dicts with protected ports configuration.

    OLH: olhProtectedPorts
    """
    sw.navigate('security', 'protected_ports')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-protected-ports').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
