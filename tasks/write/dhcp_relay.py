"""Write operations for DHCP relay configuration."""
from tasks import ArubaSwitch


def add_dhcp_server(sw: ArubaSwitch, server_ip: str) -> bool:
    """Add a DHCP relay server IP. Returns True if applied."""
    sw.navigate('routing', 'dhcp_relay')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#dhcp-server-conf-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    inp = modal.query_selector("#updateServerAddress")
    if not inp:
        raise RuntimeError("Server IP input not found")
    inp.fill(server_ip)
    modal.query_selector("#modalAddButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_dhcp_server(sw: ArubaSwitch, server_ip: str) -> bool:
    """Remove a DHCP relay server. Returns True if removed, False if not found."""
    sw.navigate('routing', 'dhcp_relay')
    sw.page.click("#dhcp-server-conf-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-dhcp-server-conf').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.serverIpAddr === '{server_ip}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-dhcp-server-conf').DataTable().row({row_idx}).select();
            document.getElementById('dhcp-server-conf-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True


def add_dhcp_interface(sw: ArubaSwitch, interface_type: str, identifier: str) -> bool:
    """Add a DHCP relay interface.

    Args:
        interface_type: 'vlan' or 'port'
        identifier: VLAN ID (e.g. '200') or port number (e.g. '1')

    Returns:
        True if applied.
    """
    sw.navigate('routing', 'dhcp_relay')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#dhcp-interface-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    radio_id = "rdoInterfaceType_0" if interface_type == "vlan" else "rdoInterfaceType_1"
    radio = modal.query_selector(f"#{radio_id}")
    if radio:
        radio.click()
        sw.page.wait_for_timeout(500)

    if interface_type == "vlan":
        sel = modal.query_selector("#slctAddInterfaceVLAN")
        if sel:
            sel.select_option(label=identifier)
    else:
        sel = modal.query_selector("#slctAddInterfacePorts")
        if sel:
            sel.select_option(label=identifier)

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_dhcp_interface(sw: ArubaSwitch, identifier: str) -> bool:
    """Remove a DHCP relay interface. Returns True if removed, False if not found."""
    sw.navigate('routing', 'dhcp_relay')
    sw.page.click("#dhcp-interface-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-dhcp-interface').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{identifier}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-dhcp-interface').DataTable().row({row_idx}).select();
            document.getElementById('dhcp-interface-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True
