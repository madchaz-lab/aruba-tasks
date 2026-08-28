"""Write operations for DHCP snooping configuration."""
from tasks import ArubaSwitch

VLAN_TABLE = '#datagrid-dhcp-vlan-settings'
IFACE_TABLE = '#datagrid-interface-settings'
BINDING_TABLE = '#datagrid-binding-database'


def enable_dhcp_snooping(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable global DHCP snooping. Returns True if changed."""
    sw.navigate('security', 'dhcp_snooping')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkDHCPSnooping")
    if not chk:
        raise RuntimeError("DHCP snooping checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('chkDHCPSnooping').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_dhcp_trusted_port(sw: ArubaSwitch, port: int, trusted: bool = True) -> bool:
    """Set a port as DHCP trusted/untrusted. Returns True if changed."""
    sw.navigate('security', 'dhcp_snooping')
    sw.page.click("#interface-settings-refresh")
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
            document.getElementById('interface-settings-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    chk = modal.query_selector("#chkEditDHCPTrustedInterface")
    if not chk:
        raise RuntimeError("Trusted interface checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == trusted:
        modal.query_selector("#modalEditTrustModeButtonCancel").click()
        return False

    sw.page.evaluate("document.getElementById('chkEditDHCPTrustedInterface').click()")
    modal.query_selector("#modalEditTrustModeButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def add_dhcp_binding(sw: ArubaSwitch, vid: int, mac: str, ip: str, port: str,
                     infinite: bool = True) -> bool:
    """Add a static DHCP binding. Returns True if applied."""
    sw.navigate('security', 'dhcp_snooping')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#binding-database-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    vid_inp = modal.query_selector("#txtAddBindingDatabaseVLANID")
    if vid_inp:
        vid_inp.fill(str(vid))

    mac_inp = modal.query_selector("#txtAddBindingDatabaseMACAddress")
    if mac_inp:
        mac_inp.fill(mac)

    ip_inp = modal.query_selector("#txtAddBindingDatabaseIP")
    if ip_inp:
        ip_inp.fill(ip)

    port_sel = modal.query_selector("#slctAddBindingDatabaseInterface")
    if port_sel:
        port_sel.select_option(label=str(port))

    if infinite:
        sw.page.evaluate("document.getElementById('rdoAddBindingDatabaseLeaseTime_0').click()")
    else:
        sw.page.evaluate("document.getElementById('rdoAddBindingDatabaseLeaseTime_1').click()")
        sw.page.wait_for_timeout(300)

    modal.query_selector("#modalAddBindingDatabaseApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def clear_dhcp_bindings(sw: ArubaSwitch) -> bool:
    """Clear all dynamic DHCP bindings. Returns True if cleared."""
    sw.navigate('security', 'dhcp_snooping')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#binding-database-clearall-dynamic-ip")
    sw.page.wait_for_timeout(1500)

    confirm = sw.page.query_selector(".modal.show")
    if confirm:
        apply_btn = confirm.query_selector("#modalClearAllBindingDatabaseButtonApply")
        if apply_btn:
            apply_btn.click()
            sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
