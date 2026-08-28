"""Write operations for IGMP snooping configuration."""
from tasks import ArubaSwitch

VLAN_TABLE = '#datagrid-snooping_configuration_table'


def _find_vlan_row(sw: ArubaSwitch, vid: int) -> int:
    """Return DataTable row index for a VLAN ID, or -1."""
    return sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{VLAN_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{vid}')) return i;
            }}
            return -1;
        }}
    """)


def configure_igmp_snooping(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable global IGMP snooping. Returns True if changed."""
    sw.navigate('switching', 'igmp_snooping')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#global_checkbox_btn")
    if not chk:
        raise RuntimeError("Global IGMP snooping checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('global_checkbox_btn').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_igmp_querier(sw: ArubaSwitch, enable: bool = None, version: str = None,
                     election: bool = None, ip_address: str = None,
                     robustness: int = None, query_interval: int = None,
                     response_time: int = None) -> bool:
    """Configure IGMP querier settings. Returns True if applied.

    Args:
        enable: Enable/disable IGMP querier
        version: 'v2' or 'v3'
        election: Enable/disable querier election
        ip_address: Querier IP address
        robustness: Querier robustness variable
        query_interval: Query interval (seconds)
        response_time: Max response time (seconds)
    """
    sw.navigate('switching', 'igmp_snooping')
    sw.page.click("#snooping-vlan-refresh")
    sw.page.wait_for_timeout(1000)

    # Select first row to enable edit button
    sw.page.evaluate("""
        () => {
            jQuery('#datagrid-snooping_configuration_table').DataTable().row(0).select();
            document.getElementById('snooping-vlan-edit').click();
        }
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    if enable is not None:
        chk = modal.query_selector("#modalConfiAdminSwither")
        if chk:
            is_checked = chk.is_checked()
            if is_checked != enable:
                sw.page.evaluate("document.getElementById('modalConfiAdminSwither').click()")
                sw.page.wait_for_timeout(300)

    querier_chk = modal.query_selector("#igmpQuerier")
    if querier_chk:
        sw.page.evaluate("document.getElementById('igmpQuerier').click()")
        sw.page.wait_for_timeout(300)

    if version is not None:
        radio_id = "igmpQuerierVersionRadio_0" if version == "v2" else "igmpQuerierVersionRadio_1"
        radio = modal.query_selector(f"#{radio_id}")
        if radio:
            sw.page.evaluate(f"document.getElementById('{radio_id}').click()")
            sw.page.wait_for_timeout(300)

    if election is not None:
        chk = modal.query_selector("#igmpQuerierElection")
        if chk:
            is_checked = chk.is_checked()
            if is_checked != election:
                sw.page.evaluate("document.getElementById('igmpQuerierElection').click()")
                sw.page.wait_for_timeout(300)

    if ip_address is not None:
        inp = modal.query_selector("#txtAddQuerierIpAddress")
        if inp:
            inp.fill(ip_address)

    if robustness is not None:
        inp = modal.query_selector("#querierRobustness")
        if inp:
            inp.fill(str(robustness))

    if query_interval is not None:
        inp = modal.query_selector("#queryInterval")
        if inp:
            inp.fill(str(query_interval))

    if response_time is not None:
        inp = modal.query_selector("#responseTime")
        if inp:
            inp.fill(str(response_time))

    modal.query_selector("#modalEditSpnoopingVlanApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def add_static_member(sw: ArubaSwitch, vid: int, mac_address: str) -> bool:
    """Add a static multicast group member. Returns True if applied.

    Args:
        vid: VLAN ID
        mac_address: MAC address of the member
    """
    sw.navigate('switching', 'igmp_snooping')
    sw.page.click("#snooping-vlan-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = _find_vlan_row(sw, vid)
    if row_idx < 0:
        raise ValueError(f"VLAN {vid} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{VLAN_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('snooping-mrouter').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add static member modal not found")

    ms = modal.query_selector("#edit-multiselect")
    if ms:
        ms.select_option(label=mac_address)
    right_btn = modal.query_selector("#edit-multiselect_rightSelected")
    if right_btn:
        right_btn.click()
        sw.page.wait_for_timeout(500)

    modal.query_selector("#modalAddRoutingApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
