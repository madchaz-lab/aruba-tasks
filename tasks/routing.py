"""Routing and IP interface operations."""
from tasks import ArubaSwitch


def list_vlan_interfaces(sw: ArubaSwitch):
    """Return list of dicts with VLAN interface info."""
    sw.navigate('routing', 'routing_config')
    sw.page.wait_for_timeout(2000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-routing-vlan').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                const row = dt.row(i);
                result.push(row.data());
            }
            return result;
        }
    """)


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

    # Click the 'None' radio button label
    label = modal.query_selector("#lblrbVlanIPAddressMethod_0")
    if label:
        label.click()
        sw.page.wait_for_timeout(500)

    # Clear IP and mask fields
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

    # Click 'Manual' radio button
    label = modal.query_selector("#lblrbVlanIPAddressMethod_1")
    if label:
        label.click()
        sw.page.wait_for_timeout(500)

    # Set IP and mask
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
