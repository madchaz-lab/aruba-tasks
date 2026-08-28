"""Write operations for LLDP configuration."""
from tasks import ArubaSwitch

PORT_TABLE = '#datagrid-lldp-interface'


def _find_port_row(sw: ArubaSwitch, port: int) -> int:
    """Return DataTable row index for a port number, or -1."""
    return sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{PORT_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 1).data().toString().trim() === '{port}') return i;
            }}
            return -1;
        }}
    """)


def set_lldp_timers(sw: ArubaSwitch, update_interval: int = None, hold_multiplier: int = None,
                    reinit_delay: int = None, notification_interval: int = None) -> bool:
    """Set global LLDP timers. Returns True if applied.

    Args:
        update_interval: Time between LLDP frame transmissions (seconds)
        hold_multiplier: Multiplier for hold time
        reinit_delay: Re-initialization delay (seconds)
        notification_interval: Notification interval (seconds)
    """
    sw.navigate('neighbor_discovery', 'lldp')
    sw.page.wait_for_timeout(2000)

    if update_interval is not None:
        inp = sw.page.query_selector("#updateInterval")
        if inp:
            inp.fill(str(update_interval))

    if hold_multiplier is not None:
        inp = sw.page.query_selector("#holdMultiplier")
        if inp:
            inp.fill(str(hold_multiplier))

    if reinit_delay is not None:
        inp = sw.page.query_selector("#reinitializingDelay")
        if inp:
            inp.fill(str(reinit_delay))

    if notification_interval is not None:
        inp = sw.page.query_selector("#notificationInterval")
        if inp:
            inp.fill(str(notification_interval))

    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def configure_lldp_interface(sw: ArubaSwitch, port: int, transmit: bool = None, receive: bool = None,
                             notify: bool = None, management: bool = None, mac_phy: bool = None,
                             power: bool = None, link_agg: bool = None, max_frame: bool = None) -> bool:
    """Configure LLDP settings for a specific port. Returns True if applied.

    Args:
        port: Port number
        transmit: Enable/disable LLDP transmission
        receive: Enable/disable LLDP reception
        notify: Enable/disable notifications
        management: Enable/disable management TLV
        mac_phy: Enable/disable MAC/PHY config TLV
        power: Enable/disable Power via MDI TLV
        link_agg: Enable/disable Link Aggregation TLV
        max_frame: Enable/disable Max Frame Size TLV
    """
    sw.navigate('neighbor_discovery', 'lldp')
    sw.page.wait_for_timeout(2000)

    row_idx = _find_port_row(sw, port)
    if row_idx < 0:
        raise ValueError(f"Port {port} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{PORT_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('interface-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    checkboxes = {
        "chkTransmit": transmit,
        "chkReceive": receive,
        "chkNotify": notify,
        "chkManagement": management,
        "chkMacPhyConfigStatus": mac_phy,
        "chkPowerViaMDI": power,
        "chkLinkAggregation": link_agg,
        "chkMaxFrameSize": max_frame,
    }

    for chk_id, desired in checkboxes.items():
        if desired is None:
            continue
        chk = modal.query_selector(f"#{chk_id}")
        if chk:
            is_checked = chk.is_checked()
            if is_checked != desired:
                sw.page.evaluate(f"document.getElementById('{chk_id}').click()")
                sw.page.wait_for_timeout(300)

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
