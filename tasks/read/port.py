"""Read operations for port configuration."""
from tasks import ArubaSwitch

PORT_TABLE = '#datagrid-interface-port'


def list_ports(sw: ArubaSwitch):
    """Return list of dicts with port info.

    Columns: 0=checkbox, 1=Interface, 2=Description, 3=Type, 4=Admin Mode,
    5=Schedule, 6=Physical Mode, 7=Physical Status, 8=Auto Negotiation,
    9=STP Mode, 10=LACP Mode, 11=Link Status
    """
    sw.navigate('switching', 'port_config')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{PORT_TABLE}').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {{
                result.push({{
                    port: dt.cell(i, 1).data(),
                    description: dt.cell(i, 2).data(),
                    type: dt.cell(i, 3).data(),
                    status: dt.cell(i, 11).data()
                }});
            }}
            return result;
        }}
    """)
