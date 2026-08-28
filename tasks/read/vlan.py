"""Read operations for VLAN configuration.

OLH topics: olhVLAN, olhVLANConfiguration, olhVLANDeviceView
"""
from tasks import ArubaSwitch


def list_vlans(sw: ArubaSwitch):
    """Return list of (vid, name) tuples.

    OLH: olhVLAN, olhVLANConfiguration
    Table: #datagrid-configuration
    """
    sw.navigate('vlan', 'vlan_config')
    sw.page.click("#vlan-refresh-conf")
    sw.page.wait_for_timeout(1000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-configuration').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push([
                    dt.cell(i, 1).data(),
                    dt.cell(i, 2).data()
                ]);
            }
            return result;
        }
    """)


def get_vlan_device_view(sw: ArubaSwitch):
    """Return list of dicts with VLAN device view (ports per VLAN).

    OLH: olhVLANDeviceView
    Table: #datagrid-configuration
    """
    sw.navigate('vlan', 'vlan_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-configuration').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
