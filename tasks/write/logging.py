"""Write operations for logging configuration."""
from tasks import ArubaSwitch


def enable_logging(sw: ArubaSwitch, enable: bool = True) -> bool:
    """Enable or disable global logging. Returns True if changed."""
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkGlobalLogSettings")
    if not chk:
        raise RuntimeError("Global logging checkbox not found")

    is_checked = chk.is_checked()
    if is_checked == enable:
        return False

    sw.page.evaluate("document.getElementById('chkGlobalLogSettings').click()")
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def set_log_severity(sw: ArubaSwitch, level: str) -> bool:
    """Set logging severity threshold.

    Args:
        level: One of 'debug', 'info', 'notice', 'warning', 'error', 'critical', 'alert', 'emergency'
               (case-insensitive)

    Returns:
        True if applied.
    """
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(2000)

    sel = sw.page.query_selector("#slctSeverityThreshold")
    if not sel:
        raise RuntimeError("Severity threshold selector not found")

    # Switch uses capitalized labels
    level_map = {
        "debug": "Debug", "info": "Info", "notice": "Notice", "warning": "Warning",
        "error": "Error", "critical": "Critical", "alert": "Alert", "emergency": "Emergency",
    }
    label = level_map.get(level.lower(), level)
    sel.select_option(label=label)
    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def add_remote_log_server(sw: ArubaSwitch, server_ip: str, udp_port: int = 514, server_type: str = "primary") -> bool:
    """Add a remote syslog server.

    Args:
        server_ip: IP address of syslog server
        udp_port: UDP port (default 514)
        server_type: 'primary' or 'secondary'

    Returns:
        True if applied.
    """
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkRemoteLogServer")
    if chk and not chk.is_checked():
        sw.page.evaluate("document.getElementById('chkRemoteLogServer').click()")
        sw.page.wait_for_timeout(1000)

    ip_inp = sw.page.query_selector("#txtServerAddress")
    if ip_inp:
        ip_inp.fill(server_ip)

    port_inp = sw.page.query_selector("#txtinputUDPPort")
    if port_inp:
        port_inp.fill(str(udp_port))

    sel = sw.page.query_selector("#slctRemoteLogServer")
    if sel:
        sel.select_option(label=server_type)

    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True


def remove_remote_log_server(sw: ArubaSwitch) -> bool:
    """Remove remote syslog server by disabling and clearing fields. Returns True if applied."""
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(2000)

    chk = sw.page.query_selector("#chkRemoteLogServer")
    if chk and chk.is_checked():
        sw.page.evaluate("document.getElementById('chkRemoteLogServer').click()")
        sw.page.wait_for_timeout(1000)

    ip_inp = sw.page.query_selector("#txtServerAddress")
    if ip_inp:
        ip_inp.fill("")

    port_inp = sw.page.query_selector("#txtinputUDPPort")
    if port_inp:
        port_inp.fill("")

    sw.page.wait_for_timeout(1000)
    sw.apply_pending()
    return True
