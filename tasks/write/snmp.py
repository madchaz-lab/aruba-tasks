"""Write operations for SNMP configuration."""
from tasks import ArubaSwitch

COMMUNITY_TABLE = '#datagrid-community-configuration'
TRAPV1V2_TABLE = '#datagrid-trap-receivers-v1v2'
TRAPV3_TABLE = '#datagrid-trap-receivers-v3'


def enable_snmp(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable SNMP globally. Returns True if changed."""
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkSNMP")
    if not chk:
        raise RuntimeError("SNMP checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('chkSNMP').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def add_snmp_community(sw: ArubaSwitch, name: str, ip_address: str = "",
                       community_type: str = "v1v2", access: str = "read-only",
                       view: str = "", group: str = "") -> bool:
    """Add an SNMP community string. Returns True if applied.

    Args:
        name: Community name
        ip_address: Allowed IP address (empty for any)
        community_type: 'v1v2' or 'v3'
        access: 'read-only', 'read-write', or 'notify'
        view: View name
        group: Group name
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#community-configuration-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    name_inp = modal.query_selector("#txtAddCommunityName")
    if name_inp:
        name_inp.fill(name)

    ip_inp = modal.query_selector("#txtAddIpAddress")
    if ip_inp:
        ip_inp.fill(ip_address)

    type_radio = "rdoAddCommunityType_0" if community_type == "v1v2" else "rdoAddCommunityType_1"
    sw.page.evaluate(f"document.getElementById('{type_radio}').click()")
    sw.page.wait_for_timeout(500)

    access_map = {"read-only": "rdoAddCommunityAccess_0", "read-write": "rdoAddCommunityAccess_1", "notify": "rdoAddCommunityAccess_2"}
    access_radio = access_map.get(access, "rdoAddCommunityAccess_0")
    sw.page.evaluate(f"document.getElementById('{access_radio}').click()")
    sw.page.wait_for_timeout(500)

    view_inp = modal.query_selector("#txtAddCommunityView")
    if view_inp and view:
        view_inp.fill(view)

    group_sel = modal.query_selector("#slcAddCommunityGroup")
    if group_sel and group:
        group_sel.select_option(label=group)

    modal.query_selector("#modalAddCommunityButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_snmp_community(sw: ArubaSwitch, name: str) -> bool:
    """Remove an SNMP community string. Returns True if removed, False if not found."""
    sw.navigate('switching', 'snmp')
    sw.page.click("#community-configuration-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{COMMUNITY_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{name}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('{COMMUNITY_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('community-configuration-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True


def add_snmp_trap_receiver(sw: ArubaSwitch, ip_address: str, community_name: str = "",
                           snmp_version: str = "v1v2", notify_type: str = "trap",
                           udp_port: int = 162, timeout: int = 5, retries: int = 3) -> bool:
    """Add an SNMP trap receiver. Returns True if applied.

    Args:
        ip_address: Receiver IP address
        community_name: Community name for v1/v2
        snmp_version: 'v1v2' (uses TRAPV1V2_TABLE)
        notify_type: 'trap' or 'inform'
        udp_port: UDP port
        timeout: Timeout in seconds
        retries: Number of retries
    """
    sw.navigate('switching', 'snmp')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#trap-receivers-v1v2-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    ip_inp = modal.query_selector("#txtAddTrapV1V2IpAddress")
    if ip_inp:
        ip_inp.fill(ip_address)

    comm_inp = modal.query_selector("#txtAddTrapV1V2CommunityName")
    if comm_inp and community_name:
        comm_inp.fill(community_name)

    notify_radio = "rdoAddTrapV1V2NotifyType_0" if notify_type == "trap" else "rdoAddTrapV1V2NotifyType_1"
    sw.page.evaluate(f"document.getElementById('{notify_radio}').click()")
    sw.page.wait_for_timeout(500)

    ver_radio = "rdoAddTrapV1V2SNMPVersion_0" if snmp_version == "v1" else "rdoAddTrapV1V2SNMPVersion_1"
    sw.page.evaluate(f"document.getElementById('{ver_radio}').click()")
    sw.page.wait_for_timeout(500)

    timeout_inp = modal.query_selector("#txtAddTrapV1V2Timeout")
    if timeout_inp and timeout_inp.is_enabled():
        timeout_inp.fill(str(timeout))

    retries_inp = modal.query_selector("#txtAddTrapV1V2Retries")
    if retries_inp and retries_inp.is_enabled():
        retries_inp.fill(str(retries))

    port_inp = modal.query_selector("#txtAddTrapV1V2UDPPort")
    if port_inp:
        port_inp.fill(str(udp_port))

    modal.query_selector("#modalAddTrapReceiversV1V2ButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_snmp_trap_receiver(sw: ArubaSwitch, ip_address: str) -> bool:
    """Remove an SNMP trap receiver. Returns True if removed, False if not found."""
    sw.navigate('switching', 'snmp')
    sw.page.click("#trap-receivers-v1v2-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{TRAPV1V2_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{ip_address}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('{TRAPV1V2_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('trap-receivers-v1v2-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True
