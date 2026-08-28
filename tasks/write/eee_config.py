"""Write operations for Energy Efficient Ethernet (EEE) configuration."""
from tasks import ArubaSwitch


def enable_ee(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable EEE on auto-negotiated ports. Returns True if changed."""
    sw.navigate('switching', 'eee_config')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkAutoPort")
    if not chk:
        raise RuntimeError("EEE auto-port checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('chkAutoPort').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def enable_low_power(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable low power mode. Returns True if changed."""
    sw.navigate('switching', 'eee_config')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkLowPower")
    if not chk:
        raise RuntimeError("Low power checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    chk.click()
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True
