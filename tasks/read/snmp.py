"""Read operations for SNMP configuration.

OLH topics: olhSNMP, olhSNMPCommunities, olhSNMPUsers, olhSNMPV3Receivers,
            olhSNMPEngineID, olhSNMPFilters, olhSNMPViews, olhSNMPV1V2Receivers
"""
from tasks import ArubaSwitch


def get_snmp_settings(sw: ArubaSwitch):
    """Return dict with SNMP global settings.

    OLH: olhSNMP
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def list_snmp_communities(sw: ArubaSwitch):
    """Return list of dicts with SNMP community configuration.

    OLH: olhSNMPCommunities
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-snmp-community').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_snmp_users(sw: ArubaSwitch):
    """Return list of dicts with SNMP user configuration.

    OLH: olhSNMPUsers
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-snmp-user').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_snmp_v3_receivers(sw: ArubaSwitch):
    """Return list of dicts with SNMP v3 receiver configuration.

    OLH: olhSNMPV3Receivers
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-snmp-v3-receiver').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_snmp_engine_id(sw: ArubaSwitch):
    """Return dict with SNMP engine ID.

    OLH: olhSNMPEngineID
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Engine ID')) {
                    if (i + 1 < lines.length) {
                        result.engine_id = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def list_snmp_filters(sw: ArubaSwitch):
    """Return list of dicts with SNMP filter configuration.

    OLH: olhSNMPFilters
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-snmp-filter').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_snmp_views(sw: ArubaSwitch):
    """Return list of dicts with SNMP view configuration.

    OLH: olhSNMPViews
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-snmp-view').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_snmp_v1v2_receivers(sw: ArubaSwitch):
    """Return list of dicts with SNMP v1/v2 receiver configuration.

    OLH: olhSNMPV1V2Receivers
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-snmp-v1v2-receiver').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
