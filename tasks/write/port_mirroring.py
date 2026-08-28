"""Write operations for port mirroring configuration."""
from tasks import ArubaSwitch

MIRROR_TABLE = '#datagrid-portDatagridInterface'


def add_mirror_session(sw: ArubaSwitch, session_id: str, probe_port: str,
                       source_type: str, source: str, direction: str = "both") -> bool:
    """Add a port mirror session. Returns True if applied.

    Args:
        session_id: Session ID number
        probe_port: Destination port for mirrored traffic
        source_type: 'port' or 'vlan'
        source: Source port or VLAN ID
        direction: 'inbound', 'outbound', or 'both'
    """
    sw.navigate('switching', 'port_mirroring')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkPortMirroringGC")
    if chk and not chk.is_checked():
        sw.page.evaluate("document.getElementById('chkPortMirroringGC').click()")
        sw.page.wait_for_timeout(500)

    sw.page.evaluate("document.getElementById('mirroring-add').click()")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    sel = modal.query_selector("#modalSessId")
    if sel:
        sel.select_option(value="New Session")

    port_sel = modal.query_selector("#addSessionProbePortName_1")
    if port_sel:
        port_sel.select_option(label=probe_port)

    radio_id = "addSourceTypeName_0" if source_type == "port" else "addSourceTypeName_1"
    sw.page.evaluate(f"document.getElementById('{radio_id}').click()")
    sw.page.wait_for_timeout(500)

    source_sel = modal.query_selector("#addSourcePortName")
    if source_sel:
        source_sel.select_option(label=source)

    dir_map = {"inbound": "addDirectionName_0", "outbound": "addDirectionName_1", "both": "addDirectionName_2"}
    dir_radio = dir_map.get(direction, "addDirectionName_2")
    sw.page.evaluate(f"document.getElementById('{dir_radio}').click()")
    sw.page.wait_for_timeout(500)

    modal.query_selector("#modalAddApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def edit_mirror_session(sw: ArubaSwitch, session_id: str, probe_port: str = None,
                        source_type: str = None, source: str = None, direction: str = None) -> bool:
    """Edit an existing mirror session. Returns True if applied."""
    sw.navigate('switching', 'port_mirroring')
    sw.page.click("#mirroring-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{MIRROR_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{session_id}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"Mirror session {session_id} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{MIRROR_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('mirroring-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    if probe_port is not None:
        port_sel = modal.query_selector("#editSessionProbePortName")
        if port_sel:
            port_sel.select_option(label=probe_port)

    if source_type is not None:
        radio_id = "editSourceTypeName_0" if source_type == "port" else "editSourceTypeName_1"
        sw.page.evaluate(f"document.getElementById('{radio_id}').click()")
        sw.page.wait_for_timeout(500)

    if source is not None:
        source_sel = modal.query_selector("#editSourcePortName")
        if source_sel:
            source_sel.select_option(label=source)

    if direction is not None:
        dir_map = {"inbound": "editDirectionName_0", "outbound": "editDirectionName_1", "both": "editDirectionName_2"}
        dir_radio = dir_map.get(direction, "editDirectionName_2")
        sw.page.evaluate(f"document.getElementById('{dir_radio}').click()")
        sw.page.wait_for_timeout(500)

    modal.query_selector("#modalEditApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_mirror_session(sw: ArubaSwitch, session_id: str) -> bool:
    """Remove a port mirror session. Returns True if removed, False if not found."""
    sw.navigate('switching', 'port_mirroring')
    sw.page.click("#mirroring-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{MIRROR_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{session_id}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('{MIRROR_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('mirroring-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True
