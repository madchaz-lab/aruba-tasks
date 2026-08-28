"""Read operations for RADIUS configuration.

OLH topics: olhRADIUS, olhRADIUSServer, olhRADIUSServers
"""
from tasks import ArubaSwitch


def list_radius_servers(sw: ArubaSwitch):
    """Return list of dicts with RADIUS server configuration.

    OLH: olhRADIUS
    """
    sw.navigate('security', 'radius')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-radius-server').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_radius_global(sw: ArubaSwitch):
    """Return dict with RADIUS global settings.

    OLH: olhRADIUS
    """
    sw.navigate('security', 'radius')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)
