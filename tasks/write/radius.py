"""Write operations for RADIUS server configuration."""
from tasks import ArubaSwitch

RADIUS_TABLE = '#datagrid-radius-server'


def add_radius_server(sw: ArubaSwitch, server_ip: str, auth_port: int = 1812,
                      acct_port: int = 1813, priority: int = 1, secret: str = "",
                      force_mac: bool = False) -> bool:
    """Add a RADIUS server. Returns True if applied."""
    sw.navigate('security', 'radius')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#add-radius-server")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    ip_inp = modal.query_selector("#txtAddServerIP")
    if ip_inp:
        ip_inp.fill(server_ip)

    auth_inp = modal.query_selector("#txtAddAuthenticationPort")
    if auth_inp:
        auth_inp.fill(str(auth_port))

    acct_inp = modal.query_selector("#txtAddAccountingPort")
    if acct_inp:
        acct_inp.fill(str(acct_port))

    pri_inp = modal.query_selector("#txtAddServerPriority")
    if pri_inp:
        pri_inp.fill(str(priority))

    secret_inp = modal.query_selector("#txtAddSecret")
    if secret_inp and secret:
        secret_inp.fill(secret)

    if force_mac:
        sw.page.evaluate("document.getElementById('chkAddRadiusForceMA').click()")
        sw.page.wait_for_timeout(300)

    modal.query_selector("#modalAddButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def edit_radius_server(sw: ArubaSwitch, server_ip: str, auth_port: int = None,
                       acct_port: int = None, priority: int = None,
                       secret: str = None, force_mac: bool = None) -> bool:
    """Edit an existing RADIUS server. Returns True if applied."""
    sw.navigate('security', 'radius')
    sw.page.click("#radius-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{RADIUS_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{server_ip}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"RADIUS server {server_ip} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('{RADIUS_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('radius-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit modal not found")

    if auth_port is not None:
        inp = modal.query_selector("#txtEditAuthenticationPort")
        if inp:
            inp.fill(str(auth_port))

    if acct_port is not None:
        inp = modal.query_selector("#txtEditAccountingPort")
        if inp:
            inp.fill(str(acct_port))

    if priority is not None:
        inp = modal.query_selector("#txtEditServerPriority")
        if inp:
            inp.fill(str(priority))

    if secret is not None:
        sw.page.evaluate("document.getElementById('rdoSecret_1').click()")
        sw.page.wait_for_timeout(300)
        inp = modal.query_selector("#txtEditSecretInput")
        if inp:
            inp.fill(secret)

    if force_mac is not None:
        chk = modal.query_selector("#chkEditRadiusForceMA")
        if chk:
            is_checked = chk.is_checked()
            if is_checked != force_mac:
                sw.page.evaluate("document.getElementById('chkEditRadiusForceMA').click()")
                sw.page.wait_for_timeout(300)

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_radius_server(sw: ArubaSwitch, server_ip: str) -> bool:
    """Remove a RADIUS server. Returns True if removed, False if not found."""
    sw.navigate('security', 'radius')
    sw.page.click("#radius-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{RADIUS_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{server_ip}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('{RADIUS_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('radius-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True
