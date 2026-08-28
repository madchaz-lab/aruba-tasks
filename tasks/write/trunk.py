"""Write operations for trunk configuration.

Note: Aruba Instant On 1930 web UI does NOT support trunk removal.
Trunks can only be disabled and have member ports removed.
"""
from tasks import ArubaSwitch


def disable_trunk(sw: ArubaSwitch, trunk_num: int) -> bool:
    """Disable a trunk group. Returns True if disabled."""
    sw.navigate('switching', 'trunk_config')
    sw.page.wait_for_timeout(3000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-trunks').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 1).data().toString().includes('TRK{trunk_num}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"TRK{trunk_num} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-trunks').DataTable().row({row_idx}).select();
            document.getElementById('trunks-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    chk = modal.query_selector("#chkAdminMode")
    if chk and chk.is_checked():
        chk.click()
        sw.page.wait_for_timeout(500)

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def clear_trunk_members(sw: ArubaSwitch, trunk_num: int) -> bool:
    """Remove all member ports from a trunk. Returns True if applied."""
    sw.navigate('switching', 'trunk_config')
    sw.page.wait_for_timeout(3000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-trunks').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 1).data().toString().includes('TRK{trunk_num}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"TRK{trunk_num} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-trunks').DataTable().row({row_idx}).select();
            document.getElementById('trunks-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    btn = modal.query_selector("#multiselect_leftSelected")
    if btn:
        btn.click()
        sw.page.wait_for_timeout(1000)

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
