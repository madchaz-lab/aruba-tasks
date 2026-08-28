"""Write operations for protected ports configuration."""
from tasks import ArubaSwitch

PORT_TABLE = '#datagrid-protected-ports'


def enable_protected_port(sw: ArubaSwitch, port: int, enable: bool = True) -> bool:
    """Enable or disable protected port on a specific port. Returns True if changed."""
    sw.navigate('security', 'protected_ports')
    sw.page.wait_for_timeout(2000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{PORT_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 1).data().toString().trim() === '{port}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"Port {port} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{PORT_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('protected-ports-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    chk = modal.query_selector("#chkEditProtectedPorts")
    if not chk:
        raise RuntimeError("Protected port checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        modal.query_selector("#modalEditButtonCancel").click()
        return False

    sw.page.evaluate("document.getElementById('chkEditProtectedPorts').click()")
    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
