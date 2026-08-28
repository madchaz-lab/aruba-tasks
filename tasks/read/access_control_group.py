"""Read operations for Access Control Group.

OLH topics: olhAccessControlGroup
"""
from tasks import ArubaSwitch


def list_access_control_groups(sw: ArubaSwitch):
    """Return list of dicts with access control group configuration.

    OLH: olhAccessControlGroup
    """
    sw.navigate('security', 'port_access_control')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-access-control-group').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
