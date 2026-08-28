"""Write operations for global STP configuration."""
from tasks import ArubaSwitch


def enable_stp(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable global STP. Returns True if changed."""
    sw.navigate('spanning_tree', 'stp_global')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkAdminMode")
    if not chk:
        raise RuntimeError("STP admin mode checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('chkAdminMode').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_stp_priority(sw: ArubaSwitch, priority: int) -> bool:
    """Set bridge priority. Returns True if applied.

    Args:
        priority: Bridge priority value (must be multiple of 4096, 0-61440)
    """
    sw.navigate('spanning_tree', 'stp_global')
    sw.page.wait_for_timeout(2000)

    sel = sw.page.query_selector("#slctBridgePriority")
    if not sel:
        raise RuntimeError("Bridge priority selector not found")

    sel.select_option(label=str(priority))
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_stp_timers(sw: ArubaSwitch, max_age: int = None, forward_delay: int = None) -> bool:
    """Set STP timers. Returns True if applied.

    Args:
        max_age: Max age in seconds (6-40)
        forward_delay: Forward delay in seconds (4-30)
    """
    sw.navigate('spanning_tree', 'stp_global')
    sw.page.wait_for_timeout(2000)

    if max_age is not None:
        inp = sw.page.query_selector("#updateBridgeMaxAge")
        if inp:
            inp.fill(str(max_age))

    if forward_delay is not None:
        inp = sw.page.query_selector("#updateBridgeForwardDelay")
        if inp:
            inp.fill(str(forward_delay))

    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def enable_bpdu_filter(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable BPDU filter. Returns True if changed."""
    sw.navigate('spanning_tree', 'stp_global')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkBPDUFilter")
    if not chk:
        raise RuntimeError("BPDU filter checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('chkBPDUFilter').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True
