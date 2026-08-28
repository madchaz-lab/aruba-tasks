"""Write operations for voice VLAN configuration."""
from tasks import ArubaSwitch


def add_telephony_oui(sw: ArubaSwitch, oui: str, description: str = "") -> bool:
    """Add a custom telephony OUI. Returns True if applied.

    Args:
        oui: OUI string (e.g. '00:11:22')
        description: Optional description
    """
    sw.navigate('vlan', 'voice_vlan')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#oui-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add OUI modal not found")

    oui_inp = modal.query_selector("#txtAddTelephony")
    if oui_inp:
        oui_inp.fill(oui)

    desc_inp = modal.query_selector("#txtAddDescription")
    if desc_inp:
        desc_inp.fill(description)

    sw.page.evaluate("document.getElementById('modalAddTelephonyOUIApply').click()")
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_telephony_oui(sw: ArubaSwitch, oui: str) -> bool:
    """Remove a custom telephony OUI. Returns True if removed, False if not found.

    Note: OUI can be in any format (AA:BB:CC, AA BB CC, AABBCC).
    """
    sw.navigate('vlan', 'voice_vlan')
    sw.page.click("#oui-refresh")
    sw.page.wait_for_timeout(1000)

    # Normalize OUI: switch stores as "AA BB CC", user may pass "AA:BB:CC" or "AABBCC"
    oui_normalized = oui.replace(":", " ").replace("-", " ").upper()

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-telephonyOUI').DataTable();
            const search = '{oui_normalized}';
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.OUIPrefix && data.OUIPrefix === search) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-telephonyOUI').DataTable().row({row_idx}).select();
            document.getElementById('oui-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True


def restore_telephony_oui(sw: ArubaSwitch) -> bool:
    """Restore default telephony OUI list. Returns True if applied."""
    sw.navigate('vlan', 'voice_vlan')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#oui-restore")
    sw.page.wait_for_timeout(1500)

    confirm = sw.page.query_selector(".modal.show")
    if confirm:
        apply_btn = confirm.query_selector("#modalRestoreButtonApply")
        if apply_btn:
            apply_btn.click()
            sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
