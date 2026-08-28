"""Read operations for LAG (Link Aggregation Group) configuration.

OLH topics: olhLAG, olhLAGGlobal, olhLAGInterface
Note: LAG groups are shown on the trunk_config page.
"""
from tasks import ArubaSwitch


def list_lag_groups(sw: ArubaSwitch):
    """Return list of dicts with LAG group configuration.

    OLH: olhLAG
    Table: trunk config DataTable
    """
    sw.navigate('switching', 'trunk_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-trunk-config').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
