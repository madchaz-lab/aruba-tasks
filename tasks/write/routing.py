"""Write operations for routing and VLAN IP interfaces."""
from tasks import ArubaSwitch


def clear_vlan_ip(sw: ArubaSwitch, vid: int) -> bool:
    """Clear IP address from a VLAN interface. Returns True if changed."""
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(2000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-routing-vlan').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.interfaceName && data.interfaceName.toString().includes('{vid}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"VLAN {vid} not found in routing table")

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-routing-vlan').DataTable().row({row_idx}).select();
            document.getElementById('routing-edit-vlan').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    label = modal.query_selector("#lblrbVlanIPAddressMethod_0")
    if label:
        label.click()
        sw.page.wait_for_timeout(500)

    for inp in modal.query_selector_all("input[type='text']"):
        id_attr = inp.get_attribute("id") or ""
        value = inp.get_attribute("value") or ""
        if value and ("ip" in id_attr.lower() or "mask" in id_attr.lower() or "address" in id_attr.lower()):
            inp.fill("")

    modal.query_selector("button:has-text('APPLY')").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def set_vlan_ip(sw: ArubaSwitch, vid: int, ip: str, mask: str) -> bool:
    """Set static IP on a VLAN interface. Returns True if applied."""
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(2000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-routing-vlan').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.interfaceName && data.interfaceName.toString().includes('{vid}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"VLAN {vid} not found in routing table")

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-routing-vlan').DataTable().row({row_idx}).select();
            document.getElementById('routing-edit-vlan').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    label = modal.query_selector("#lblrbVlanIPAddressMethod_1")
    if label:
        label.click()
        sw.page.wait_for_timeout(500)

    ip_input = modal.query_selector("#txtVlanIPAddress")
    mask_input = modal.query_selector("#txtVlanSubnetMask")
    if ip_input:
        ip_input.fill(ip)
    if mask_input:
        mask_input.fill(mask)

    modal.query_selector("button:has-text('APPLY')").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def add_static_route(sw: ArubaSwitch, network: str, mask: str, next_hop: str,
                     preference: int = 0, route_type: str = "network") -> bool:
    """Add a static route. Returns True if applied.

    Args:
        network: Network address
        mask: Subnet mask
        next_hop: Next hop IP address
        preference: Route preference (0-255, lower = higher priority)
        route_type: 'network', 'host', or 'default'
    """
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#add-static-route")
    sw.page.wait_for_timeout(2000)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add route modal not found")

    type_map = {"network": "rbRouteType_0", "host": "rbRouteType_1", "default": "rbRouteType_2"}
    type_radio = type_map.get(route_type, "rbRouteType_0")
    sw.page.evaluate(f"document.getElementById('{type_radio}').click()")
    sw.page.wait_for_timeout(500)

    sw.page.evaluate(f"""
        () => {{
            const net = document.getElementById('addingNetworkAddress');
            const mask = document.getElementById('addingSubnetMask');
            const hop = document.getElementById('addingNextHopIp');
            const pref = document.getElementById('addingPreference');
            if (net) net.value = '{network}';
            if (mask) mask.value = '{mask}';
            if (hop) hop.value = '{next_hop}';
            if (pref) pref.value = '{preference}';
        }}
    """)
    sw.page.wait_for_timeout(500)

    modal.query_selector("#modalAddButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_static_route(sw: ArubaSwitch, network: str) -> bool:
    """Remove a static route by network address. Returns True if removed, False if not found."""
    sw.navigate('routing', 'routing_config')
    sw.page.click("#refresh-static-route")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-routing-static').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{network}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-routing-static').DataTable().row({row_idx}).select();
            document.getElementById('remove-static-route').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True
