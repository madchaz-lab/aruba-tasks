"""Read operations for Port Mirroring.

OLH topics: olhPortMirroring
"""
from tasks import ArubaSwitch


def list_mirroring_sessions(sw: ArubaSwitch):
    """Return list of dicts with port mirroring sessions.

    OLH: olhPortMirroring
    """
    sw.navigate('switching', 'port_mirroring')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-port-mirroring').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
