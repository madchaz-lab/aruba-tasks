"""Write operations for VLAN configuration."""
from tasks import ArubaSwitch


def rename_vlan(sw: ArubaSwitch, vid: int, new_name: str) -> bool:
    """Rename a VLAN. Returns True if changed, False if already correct."""
    sw.navigate('vlan', 'vlan_config')
    sw.page.click("#vlan-refresh-conf")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-configuration').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 1).data().toString().trim() === '{vid}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"VLAN {vid} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-configuration').DataTable().row({row_idx}).select();
            document.getElementById('vlan-edit-conf').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    name_input = modal.query_selector("#txtEditVlanName")
    current = name_input.get_attribute("value") or ""
    if current == new_name:
        modal.query_selector("button:has-text('CANCEL')").click()
        return False

    name_input.fill(new_name)
    modal.query_selector("button:has-text('APPLY')").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def delete_vlan(sw: ArubaSwitch, vid: int) -> bool:
    """Delete a VLAN. Returns True if deleted, False if already gone.

    Note: VLAN must have no IP interface or DHCP relay configured.
    Use routing.clear_vlan_ip() first if needed.
    """
    sw.navigate('vlan', 'vlan_config')
    sw.page.click("#vlan-refresh-conf")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-configuration').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 1).data().toString().trim() === '{vid}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-configuration').DataTable().row({row_idx}).select();
            document.getElementById('vlan-remove-conf').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    confirm = sw.page.query_selector(".modal.show")
    if confirm:
        text = confirm.inner_text()
        if "can not be deleted" in text:
            ok_btn = confirm.query_selector("button:has-text('OK')")
            if ok_btn:
                ok_btn.click()
                sw.page.wait_for_timeout(1000)
            raise RuntimeError(f"Cannot delete VLAN {vid}: {text[:200]}")
        ok_btn = confirm.query_selector("button:has-text('OK')") or confirm.query_selector("button:has-text('Yes')")
        if ok_btn:
            ok_btn.click()
            sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def add_vlan(sw: ArubaSwitch, vid: int, name: str) -> bool:
    """Add a new VLAN. Returns True if added."""
    sw.navigate('vlan', 'vlan_config')

    sw.page.click("#vlan-add-conf")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    vid_input = modal.query_selector("#txtAddVlanId")
    name_input = modal.query_selector("#txtAddVlanName")
    vid_input.fill(str(vid))
    name_input.fill(name)
    modal.query_selector("button:has-text('APPLY')").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
