"""Write operations for port access control (MAC authentication) configuration."""
from tasks import ArubaSwitch

PORT_CONFIG_TABLE = '#datagrid-port-configuration'
VLAN_AUTH_TABLE = '#datagrid-vlan-authentication'
SUPPLICANT_TABLE = '#datagrid-supplicant-credentials'


def add_mac_auth_rule(sw: ArubaSwitch, port: int, control_mode: str = "auto",
                      quiet_period: int = 30, transmit_period: int = 30,
                      supplicant_timeout: int = 30, server_timeout: int = 30,
                      max_requests: int = 2, reauth_period: int = 3600,
                      max_users: int = 1) -> bool:
    """Configure MAC authentication on a port. Returns True if applied.

    Args:
        port: Port number
        control_mode: 'auto', 'force_authorized', or 'force_unauthorized'
        quiet_period: Quiet period in seconds
        transmit_period: Transmit period in seconds
        supplicant_timeout: Supplicant timeout in seconds
        server_timeout: Server timeout in seconds
        max_requests: Maximum requests
        reauth_period: Re-authentication period in seconds
        max_users: Maximum users
    """
    sw.navigate('security', 'port_access_control')
    sw.page.click("#port-configuration-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{PORT_CONFIG_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 0).data().toString().trim() === '{port}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"Port {port} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{PORT_CONFIG_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('port-configuration-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    mode_map = {"auto": "0", "force_authorized": "1", "force_unauthorized": "2"}
    mode_val = mode_map.get(control_mode, "0")
    sw.page.evaluate(f"""
        () => {{
            jQuery('#slcEditPortConfigurationControlMode').val('{mode_val}').trigger('change');
        }}
    """)
    sw.page.wait_for_timeout(500)

    sw.page.evaluate(f"""
        () => {{
            const quiet = document.getElementById('txtEditPortConfigurationQuietPeriod');
            const transmit = document.getElementById('txtEditPortConfigurationTransmitPeriod');
            const suppTimeout = document.getElementById('txtEditPortConfigurationSupplicantTimeout');
            const srvTimeout = document.getElementById('txtEditPortConfigurationServerTimeout');
            const maxReq = document.getElementById('txtEditPortConfigurationMaximumRequests');
            const reauth = document.getElementById('txtEditPortConfigurationReAuthenticationPeriod');
            const maxUsers = document.getElementById('txtEditPortConfigurationMaximumUsers');
            if (quiet) quiet.value = '{quiet_period}';
            if (transmit) transmit.value = '{transmit_period}';
            if (suppTimeout) suppTimeout.value = '{supplicant_timeout}';
            if (srvTimeout) srvTimeout.value = '{server_timeout}';
            if (maxReq) maxReq.value = '{max_requests}';
            if (reauth) reauth.value = '{reauth_period}';
            if (maxUsers) maxUsers.value = '{max_users}';
        }}
    """)
    sw.page.wait_for_timeout(500)

    modal.query_selector("#modalEditPortConfigurationButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_mac_auth_rule(sw: ArubaSwitch, port: int) -> bool:
    """Reset MAC authentication on a port to defaults. Returns True if applied."""
    sw.navigate('security', 'port_access_control')
    sw.page.click("#port-configuration-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{PORT_CONFIG_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 0).data().toString().trim() === '{port}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"Port {port} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{PORT_CONFIG_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('port-configuration-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    # Reset to defaults
    sw.page.evaluate("""
        () => {
            jQuery('#slcEditPortConfigurationControlMode').val('0').trigger('change');
            const quiet = document.getElementById('txtEditPortConfigurationQuietPeriod');
            const transmit = document.getElementById('txtEditPortConfigurationTransmitPeriod');
            const suppTimeout = document.getElementById('txtEditPortConfigurationSupplicantTimeout');
            const srvTimeout = document.getElementById('txtEditPortConfigurationServerTimeout');
            const maxReq = document.getElementById('txtEditPortConfigurationMaximumRequests');
            if (quiet) quiet.value = '30';
            if (transmit) transmit.value = '30';
            if (suppTimeout) suppTimeout.value = '30';
            if (srvTimeout) srvTimeout.value = '30';
            if (maxReq) maxReq.value = '2';
        }
    """)
    sw.page.wait_for_timeout(500)

    modal.query_selector("#modalEditPortConfigurationButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def add_mac_auth_group(sw: ArubaSwitch, name: str, username: str,
                       password: str = "", description: str = "") -> bool:
    """Add a supplicant credential group. Returns True if applied.

    Args:
        name: Group name
        username: Username
        password: Password (empty to use username as password)
        description: Description
    """
    sw.navigate('security', 'port_access_control')
    sw.page.evaluate("document.getElementById('supplicant-credentials-add').click()")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    sw.page.evaluate(f"""
        () => {{
            const name = document.getElementById('txtAddSupplicantCredentialsName');
            const username = document.getElementById('txtAddSupplicantCredentialsUsername');
            const password = document.getElementById('txtAddSupplicantCredentialsPassword');
            const desc = document.getElementById('txtAddSupplicantCredentialsDescription');
            if (name) name.value = '{name}';
            if (username) username.value = '{username}';
            if (password) password.value = '{password}';
            if (desc) desc.value = '{description}';
        }}
    """)
    sw.page.wait_for_timeout(500)

    modal.query_selector("#modalAddSupplicantCredentialsButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_mac_auth_group(sw: ArubaSwitch, name: str) -> bool:
    """Remove a supplicant credential group. Returns True if removed, False if not found."""
    sw.navigate('security', 'port_access_control')
    sw.page.click("#supplicant-credentials-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{SUPPLICANT_TABLE}').DataTable();
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
            jQuery('{SUPPLICANT_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('supplicant-credentials-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True


def set_vlan_authentication(sw: ArubaSwitch, vid: int, enable: bool = True) -> bool:
    """Enable or disable VLAN authentication. Returns True if applied.

    Args:
        vid: VLAN ID
        enable: Enable or disable authentication
    """
    sw.navigate('security', 'port_access_control')
    sw.page.click("#vlan-authentication-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{VLAN_AUTH_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                if (dt.cell(i, 0).data().toString().trim() === '{vid}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"VLAN {vid} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{VLAN_AUTH_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('vlan-authentication-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    chk = modal.query_selector("#chkEditVlanAuthenticationEnabled")
    if chk:
        is_checked = chk.is_checked()
        if is_checked != enable:
            sw.page.evaluate("document.getElementById('chkEditVlanAuthenticationEnabled').click()")
            sw.page.wait_for_timeout(500)

    modal.query_selector("#modalEditVlanAuthenticationButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True