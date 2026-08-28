"""Write operations for port configuration."""
from tasks import ArubaSwitch

PORT_TABLE = '#datagrid-interface-port'


def _find_port_row(sw: ArubaSwitch, port: int) -> int:
    """Return DataTable row index for a port number, or -1."""
    return sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{PORT_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 1).data().toString().trim() === '{port}') return i;
            }}
            return -1;
        }}
    """)


def _open_port_edit(sw: ArubaSwitch, port: int):
    """Select a port row and open the edit modal."""
    row_idx = _find_port_row(sw, port)
    if row_idx < 0:
        raise ValueError(f"Port {port} not found")
    sw.page.evaluate(f"""
        () => {{
            jQuery('{PORT_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('edit-interface').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")
    return modal


def edit_port_pvid(sw: ArubaSwitch, port: int, pvid: int) -> bool:
    """Set PVID for a port. Returns True if applied."""
    sw.navigate('switching', 'port_config')
    sw.page.wait_for_timeout(4000)
    modal = _open_port_edit(sw, port)

    for inp in modal.query_selector_all("input[type='text']"):
        id_attr = inp.get_attribute("id") or ""
        if "pvid" in id_attr.lower():
            inp.fill(str(pvid))

    for sel in modal.query_selector_all("select"):
        id_attr = sel.get_attribute("id") or ""
        if "pvid" in id_attr.lower():
            sel.select_option(label=str(pvid))

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def set_port_description(sw: ArubaSwitch, port: int, description: str) -> bool:
    """Set port description. Returns True if applied."""
    sw.navigate('switching', 'port_config')
    sw.page.wait_for_timeout(4000)
    modal = _open_port_edit(sw, port)

    for inp in modal.query_selector_all("input[type='text']"):
        id_attr = inp.get_attribute("id") or ""
        if "desc" in id_attr.lower():
            inp.fill(description)

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
