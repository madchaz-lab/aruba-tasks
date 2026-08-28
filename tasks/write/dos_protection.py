"""Write operations for DoS protection configuration."""
from tasks import ArubaSwitch

SYN_TABLE = '#datagrid-syntable'
IFACE_TABLE = '#datagrid-interface-settings-dsp'


def enable_dos_protection(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable SYN attack protection globally. Returns True if changed."""
    sw.navigate('security', 'dos_protection')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkInterfaceLevel")
    if not chk:
        raise RuntimeError("DoS protection checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('chkInterfaceLevel').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_dos_threshold(sw: ArubaSwitch, port: int, enable: bool = True, syn_rate: int = None) -> bool:
    """Set DoS protection settings for a specific port. Returns True if applied.

    Args:
        port: Port number
        enable: Enable/disable protection on this port
        syn_rate: SYN rate threshold (packets per second)
    """
    sw.navigate('security', 'dos_protection')
    sw.page.wait_for_timeout(2000)

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

    atk_chk = modal.query_selector("#attackPreventionModalName")
    if atk_chk:
        is_checked = atk_chk.is_checked()
        if is_checked != enable:
            sw.page.evaluate("document.getElementById('attackPreventionModalName').click()")
            sw.page.wait_for_timeout(300)

    if syn_rate is not None:
        syn_chk = modal.query_selector("#synRateModalName")
        if syn_chk:
            sw.page.evaluate("document.getElementById('synRateModalName').click()")
            sw.page.wait_for_timeout(300)
        rate_inp = modal.query_selector("#protectionThresholdName")
        if rate_inp:
            rate_inp.fill(str(syn_rate))

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
