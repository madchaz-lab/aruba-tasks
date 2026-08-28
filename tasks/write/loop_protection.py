"""Write operations for loop protection configuration."""
from tasks import ArubaSwitch

PORT_TABLE = '#datagrid-interface-loop'


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


def enable_loop_protection(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable global loop protection. Returns True if changed."""
    sw.navigate('switching', 'loop_protection')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkLoopProtection")
    if not chk:
        raise RuntimeError("Global loop protection checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate(f"document.getElementById('chkLoopProtection').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_loop_protection_time(sw: ArubaSwitch, transmission_time: int) -> bool:
    """Set global transmission time for loop protection (seconds). Returns True if applied."""
    sw.navigate('switching', 'loop_protection')
    sw.page.wait_for_timeout(2000)

    inp = sw.page.query_selector("#txtTransmissionTime")
    if not inp:
        raise RuntimeError("Transmission time input not found")

    current = inp.get_attribute("value") or ""
    if current == str(transmission_time):
        return False

    inp.fill(str(transmission_time))
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_port_loop_protection(sw: ArubaSwitch, port: int, enable: bool = True) -> bool:
    """Enable or disable loop protection on a specific port. Returns True if changed."""
    sw.navigate('switching', 'loop_protection')
    sw.page.wait_for_timeout(2000)

    row_idx = _find_port_row(sw, port)
    if row_idx < 0:
        raise ValueError(f"Port {port} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{PORT_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('interface-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    chk = modal.query_selector("#chkEditLoopProtection")
    if not chk:
        raise RuntimeError("Port loop protection checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        modal.query_selector("#modalEditButtonCancel").click()
        return False

    sw.page.evaluate("document.getElementById('chkEditLoopProtection').click()")
    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
