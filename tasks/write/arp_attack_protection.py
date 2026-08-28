"""Write operations for ARP attack protection configuration."""
from tasks import ArubaSwitch

IFACE_TABLE = '#ARPInterfaceSettingsTable'
ACCESS_TABLE = '#ARPAccessControlRulesTable'


def enable_arp_protection(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable global ARP attack protection. Returns True if changed."""
    sw.navigate('security', 'arp_attack_protection')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkARPAttackProtection")
    if not chk:
        raise RuntimeError("ARP attack protection checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('chkARPAttackProtection').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_arp_interface_protection(sw: ArubaSwitch, port: int, enable: bool = True) -> bool:
    """Enable or disable ARP protection on a specific port. Returns True if changed."""
    sw.navigate('security', 'arp_attack_protection')
    sw.page.click("#arp-interface-settings-refresh")
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
            document.getElementById('arp-interface-settings-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    chk = modal.query_selector("#chkARPInterfaceSettings")
    if not chk:
        raise RuntimeError("ARP interface checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        modal.query_selector("#modalEditButtonCancel").click()
        return False

    sw.page.evaluate("document.getElementById('chkARPInterfaceSettings').click()")
    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def add_arp_access_rule(sw: ArubaSwitch, list_type: str, name: str, ip: str, mac: str) -> bool:
    """Add an ARP access control rule. Returns True if applied.

    Args:
        list_type: 'whitelist' or 'blacklist'
        name: List name
        ip: IP address
        mac: MAC address
    """
    sw.navigate('security', 'arp_attack_protection')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#arp-access-control-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    radio_id = "rdoModalARPAccessControlRulesListType_0" if list_type == "whitelist" else "rdoModalARPAccessControlRulesListType_1"
    sw.page.evaluate(f"document.getElementById('{radio_id}').click()")
    sw.page.wait_for_timeout(500)

    name_inp = modal.query_selector("#txtARPAccessControlRulesListName")
    if name_inp:
        name_inp.fill(name)

    ip_inp = modal.query_selector("#txtARPAccessControlRulesIP")
    if ip_inp:
        ip_inp.fill(ip)

    mac_inp = modal.query_selector("#txtARPAccessControlRulesMACAddress")
    if mac_inp:
        mac_inp.fill(mac)

    modal.query_selector("#modalARPAccessControlRulesApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_arp_access_rule(sw: ArubaSwitch, ip: str) -> bool:
    """Remove an ARP access control rule by IP. Returns True if removed, False if not found."""
    sw.navigate('security', 'arp_attack_protection')
    sw.page.click("#arp-access-control-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{ACCESS_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{ip}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('{ACCESS_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('arp-access-control-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True
