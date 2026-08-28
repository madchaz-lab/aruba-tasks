"""Write operations for port security configuration."""
from tasks import ArubaSwitch

IFACE_TABLE = '#datagrid-interface-security'
STATIC_TABLE = '#datagrid-static-mac'


def enable_port_security(sw: ArubaSwitch, port: int, enable: bool = True,
                         max_addresses: int = None, sticky: bool = None,
                         shutdown: bool = None, trap: bool = None) -> bool:
    """Enable or disable port security on a specific port. Returns True if changed."""
    sw.navigate('security', 'port_security')
    sw.page.click("#interface-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{IFACE_TABLE}').DataTable();
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
            jQuery('{IFACE_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('interface-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    chk = modal.query_selector("#chkEditPortSecurity")
    if not chk:
        raise RuntimeError("Port security checkbox not found")

    is_checked = chk.is_checked()
    if is_checked != enable:
        sw.page.evaluate("document.getElementById('chkEditPortSecurity').click()")
        sw.page.wait_for_timeout(300)

    if max_addresses is not None:
        inp = modal.query_selector("#txtEditMaxAddress")
        if inp:
            inp.fill(str(max_addresses))

    if sticky is not None:
        chk = modal.query_selector("#chkEditStickyMode")
        if chk:
            is_checked = chk.is_checked()
            if is_checked != sticky:
                sw.page.evaluate("document.getElementById('chkEditStickyMode').click()")
                sw.page.wait_for_timeout(300)

    if shutdown is not None:
        chk = modal.query_selector("#chkEditShutdown")
        if chk:
            is_checked = chk.is_checked()
            if is_checked != shutdown:
                sw.page.evaluate("document.getElementById('chkEditShutdown').click()")
                sw.page.wait_for_timeout(300)

    if trap is not None:
        chk = modal.query_selector("#chkEditTrap")
        if chk:
            is_checked = chk.is_checked()
            if is_checked != trap:
                sw.page.evaluate("document.getElementById('chkEditTrap').click()")
                sw.page.wait_for_timeout(300)

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def add_static_mac(sw: ArubaSwitch, port: int, mac_address: str, vid: int = None, sticky: bool = False) -> bool:
    """Add a static MAC address binding. Returns True if applied."""
    sw.navigate('security', 'port_security')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#static-mac-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    port_sel = modal.query_selector("#slctAddInterface")
    if port_sel:
        port_sel.select_option(label=str(port))

    mac_inp = modal.query_selector("#txtAddMacAddress")
    if mac_inp:
        mac_inp.fill(mac_address)

    if vid is not None:
        vid_inp = modal.query_selector("#txtAddVlanId")
        if vid_inp:
            vid_inp.fill(str(vid))

    if sticky:
        sw.page.evaluate("document.getElementById('chkAddStickyMode').click()")
        sw.page.wait_for_timeout(300)

    modal.query_selector("#modalAddButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_static_mac(sw: ArubaSwitch, mac_address: str) -> bool:
    """Remove a static MAC address binding. Returns True if removed, False if not found."""
    sw.navigate('security', 'port_security')
    sw.page.click("#static-mac-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{STATIC_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{mac_address}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('{STATIC_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('static-mac-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True
