"""Write operations for CoS (Class of Service) configuration."""
from tasks import ArubaSwitch


def set_cos_priority(sw: ArubaSwitch, cos_value: int, priority: str = "default") -> bool:
    """Set priority mapping for a CoS value (0-7). Returns True if applied.

    Args:
        cos_value: CoS value (0-7)
        priority: Priority level - 'default', 'low', 'below-normal', 'normal',
                  'above-normal', 'high', 'critical', 'maximum'
    """
    if cos_value < 0 or cos_value > 7:
        raise ValueError("CoS value must be 0-7")

    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(2000)

    priority_map = {
        "default": "0", "low": "1", "below-normal": "2", "normal": "3",
        "above-normal": "4", "high": "5", "critical": "6", "maximum": "7",
    }
    priority_val = priority_map.get(priority, "3")

    sel_id = f"prioritySelect_item_{cos_value}"
    sw.page.evaluate(f"""
        () => {{
            jQuery('#{sel_id}').val('{priority_val}').trigger('change');
        }}
    """)
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_queue_scheduling(sw: ArubaSwitch, queue_id: int, method: str = "strict",
                         weight: int = None) -> bool:
    """Set scheduling method for a queue. Returns True if applied.

    Args:
        queue_id: Queue ID (0-7)
        method: 'strict' or 'wwr' (weighted weighted round-robin)
        weight: Weight value for WWR mode
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(2000)

    radio_id = f"scheduleType_{queue_id}_0" if method == "strict" else f"scheduleType_{queue_id}_1"
    sw.page.evaluate(f"document.getElementById('{radio_id}').click()")
    sw.page.wait_for_timeout(500)

    if method == "wwr" and weight is not None:
        weight_inp_id = f"wwrWeight_input_{queue_id}"
        inp = sw.page.query_selector(f"#{weight_inp_id}")
        if inp:
            inp.fill(str(weight))

    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_traffic_type(sw: ArubaSwitch, queue_id: int, traffic_type: str = "all") -> bool:
    """Set traffic type mapping for a queue. Returns True if applied.

    Args:
        queue_id: Queue ID (0-63, corresponds to port numbers)
        traffic_type: 'all', 'broadcast', 'multicast', or 'unicast'
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(2000)

    type_map = {"all": "_0", "broadcast": "_1", "multicast": "_2", "unicast": "_3"}
    suffix = type_map.get(traffic_type, "_0")
    radio_id = f"trafficSelect_{queue_id}_name{suffix}"

    sw.page.evaluate(f"document.getElementById('{radio_id}').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_interface_shaping_rate(sw: ArubaSwitch, port: int, rate: int) -> bool:
    """Set interface shaping rate for a port. Returns True if applied.

    Args:
        port: Port number
        rate: Shaping rate in Kbps
    """
    sw.navigate('qos', 'cos')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#isrc-edit")
    sw.page.wait_for_timeout(1500)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-interface-shaping').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 1).data().toString().trim() === '{port}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx >= 0:
        sw.page.evaluate(f"""
            () => {{
                jQuery('#datagrid-interface-shaping').DataTable().row({row_idx}).select();
                document.getElementById('isrc-edit').click();
            }}
        """)
        sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    rate_inp = modal.query_selector("#txtShapingRate")
    if rate_inp:
        rate_inp.fill(str(rate))

    modal.query_selector("#modalInterfaceShapingEditApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
