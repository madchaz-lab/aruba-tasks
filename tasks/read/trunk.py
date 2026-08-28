"""Read operations for trunk configuration."""
from tasks import ArubaSwitch


def list_trunks(sw: ArubaSwitch):
    """Return list of dicts with trunk info.

    Columns: 0=checkbox, 1=Trunk name, 2=Description, 3=Type, 4=Admin Mode,
    5=Link Status, 6=Members, 7=Active Ports, 8=actions
    """
    sw.navigate('switching', 'trunk_config')
    sw.page.wait_for_timeout(3000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-trunks').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push({
                    trunk: dt.cell(i, 1).data(),
                    description: dt.cell(i, 2).data(),
                    status: dt.cell(i, 4).data(),
                    members: dt.cell(i, 6).data()
                });
            }
            return result;
        }
    """)
