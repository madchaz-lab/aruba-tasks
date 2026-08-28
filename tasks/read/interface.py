"""Read operations for Interface configuration.

OLH topics: olhInterface, olhInterfaceConfiguration, olhInterfaceAutoRecovery
"""
from tasks import ArubaSwitch


def get_interface_config(sw: ArubaSwitch):
    """Return list of dicts with interface configuration.

    OLH: olhInterface
    """
    sw.navigate('switching', 'port_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-port-config').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_auto_recovery_settings(sw: ArubaSwitch):
    """Return dict with interface auto-recovery settings.

    OLH: olhInterfaceAutoRecovery
    """
    sw.navigate('switching', 'interface_auto_recovery')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)
