"""Read operations for routing and VLAN IP interfaces.

OLH topics: olhRouting, olhRoutingPortVlan, olhVLANInterfaceConfiguration
"""
from tasks import ArubaSwitch


def list_vlan_interfaces(sw: ArubaSwitch):
    """Return list of dicts with VLAN interface info.

    OLH: olhRouting, olhRoutingPortVlan
    Table: #datagrid-routing-vlan
    """
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(2000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-routing-vlan').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                const row = dt.row(i);
                result.push(row.data());
            }
            return result;
        }
    """)


def get_vlan_interface_configuration(sw: ArubaSwitch):
    """Return list of dicts with VLAN interface configuration details.

    OLH: olhVLANInterfaceConfiguration
    Table: #datagrid-routing-vlan
    """
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-routing-vlan').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                const row = dt.row(i);
                result.push(row.data());
            }
            return result;
        }
    """)
