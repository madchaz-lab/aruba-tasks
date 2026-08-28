"""Read operations for Security configuration.

OLH topics: olhPortSecurity, olhPortAccessControl, olhProtectedPorts
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
    """Return list of dicts with port access control configuration.

    OLH: olhPortAccessControl
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-port-access-control').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
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
