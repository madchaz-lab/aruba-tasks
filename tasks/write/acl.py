"""Write operations for ACL configuration."""
from tasks import ArubaSwitch

ACL_TABLE = '#datagrid-acl-list'
IPV4_RULES_TABLE = '#datagrid-ipv4acl-rules'
IPV6_RULES_TABLE = '#datagrid-ipv6acl-rules'
MAC_RULES_TABLE = '#datagrid-macacl-rules'
IFACE_BIND_TABLE = '#datagrid-interface-bound-acl'
VLAN_BIND_TABLE = '#datagrid-vlan-bound-acl'


def add_acl(sw: ArubaSwitch, name: str, acl_type: str = "ipv4") -> bool:
    """Add a new ACL. Returns True if applied.

    Args:
        name: ACL name
        acl_type: 'ipv4' or 'mac'
    """
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#acl-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add ACL modal not found")

    type_radio = "chkAddACLType_0" if acl_type == "ipv4" else "chkAddACLType_1"
    sw.page.evaluate(f"document.getElementById('{type_radio}').click()")
    sw.page.wait_for_timeout(500)

    name_inp = modal.query_selector("#txtAddACLName")
    if name_inp:
        name_inp.fill(name)

    modal.query_selector("#modalAddACLButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def add_acl_rule_ipv4(sw: ArubaSwitch, acl_name: str, sequence: int, action: str = "permit",
                      protocol: str = "", source_ip: str = "", source_mask: str = "",
                      dest_ip: str = "", dest_mask: str = "") -> bool:
    """Add an IPv4 ACL rule. Returns True if applied.

    Args:
        acl_name: ACL to add rule to
        sequence: Rule sequence number
        action: 'permit' or 'deny'
        protocol: Protocol name or number (empty for any)
        source_ip: Source IP (empty for any)
        source_mask: Source mask (empty for any)
        dest_ip: Destination IP (empty for any)
        dest_mask: Destination mask (empty for any)
    """
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(2000)

    name_sel = sw.page.query_selector("#slcACLNameIPv4")
    if name_sel:
        name_sel.select_option(label=acl_name)
        sw.page.wait_for_timeout(500)

    sw.page.click("#ipv4-rule-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add IPv4 rule modal not found")

    seq_inp = modal.query_selector("#txtIPv4SequenceNumber")
    if seq_inp:
        seq_inp.fill(str(sequence))

    action_radio = "rboIPv4Action_0" if action == "permit" else "rboIPv4Action_1"
    sw.page.evaluate(f"document.getElementById('{action_radio}').click()")
    sw.page.wait_for_timeout(500)

    match_radio = "rboIPv4MatchType_0" if protocol else "rboIPv4MatchType_1"
    sw.page.evaluate(f"document.getElementById('{match_radio}').click()")
    sw.page.wait_for_timeout(500)

    if protocol:
        proto_inp = modal.query_selector("#slctIPv4Protocol")
        if proto_inp:
            proto_inp.fill(protocol)

    sw.page.evaluate(f"""
        () => {{
            const srcIp = document.getElementById('txtIPv4SourceIP');
            const srcMask = document.getElementById('txtIPv4SourceMask');
            const dstIp = document.getElementById('txtIPv4DestIP');
            const dstMask = document.getElementById('txtIPv4DestMask');
            if (srcIp) srcIp.value = '{source_ip}';
            if (srcMask) srcMask.value = '{source_mask}';
            if (dstIp) dstIp.value = '{dest_ip}';
            if (dstMask) dstMask.value = '{dest_mask}';
        }}
    """)

    modal.query_selector("#modalAddIPv4ButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_acl_rule_ipv4(sw: ArubaSwitch, acl_name: str, sequence: int) -> bool:
    """Remove an IPv4 ACL rule. Returns True if removed, False if not found."""
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(2000)

    name_sel = sw.page.query_selector("#slcACLNameIPv4")
    if name_sel:
        name_sel.select_option(label=acl_name)
        sw.page.wait_for_timeout(500)

    sw.page.click("#ipv4-rule-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{IPV4_RULES_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{sequence}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('{IPV4_RULES_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('ipv4-rule-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True


def remove_acl(sw: ArubaSwitch, name: str) -> bool:
    """Remove an ACL. Returns True if removed, False if not found."""
    sw.navigate('qos', 'acl')
    sw.page.click("#acl-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{ACL_TABLE}').DataTable();
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
            jQuery('{ACL_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('acl-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True


def bind_acl_to_interface(sw: ArubaSwitch, ports: list, acl_name: str,
                          sequence_all: bool = True) -> bool:
    """Bind an ACL to interfaces. Returns True if applied.

    Args:
        ports: List of port numbers to bind to
        acl_name: ACL name to bind
        sequence_all: True to apply to all sequences, False to apply specific sequence
    """
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#interface-bound-acl-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Bind modal not found")

    port_sel = modal.query_selector("#mltsMemberPorts")
    if port_sel:
        for p in ports:
            port_sel.select_option(label=str(p))

    acl_sel = modal.query_selector("#slctBindACLName")
    if acl_sel:
        acl_sel.select_option(label=acl_name)

    seq_radio = "rdoBindSequenceNumber_0" if sequence_all else "rdoBindSequenceNumber_1"
    sw.page.evaluate(f"document.getElementById('{seq_radio}').click()")
    sw.page.wait_for_timeout(500)

    modal.query_selector("#modalInterfaceBindingButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def bind_acl_to_vlan(sw: ArubaSwitch, vid: int, acl_name: str,
                     sequence_all: bool = True) -> bool:
    """Bind an ACL to a VLAN. Returns True if applied."""
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#vlan-bound-acl-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Bind VLAN modal not found")

    port_sel = modal.query_selector("#mltsMemberPorts")
    if port_sel:
        port_sel.select_option(label=str(vid))

    acl_sel = modal.query_selector("#slctBindACLName")
    if acl_sel:
        acl_sel.select_option(label=acl_name)

    seq_radio = "rdoBindSequenceNumber_0" if sequence_all else "rdoBindSequenceNumber_1"
    sw.page.evaluate(f"document.getElementById('{seq_radio}').click()")
    sw.page.wait_for_timeout(500)

    modal.query_selector("#modalInterfaceBindingButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
