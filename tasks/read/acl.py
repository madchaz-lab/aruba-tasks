"""Read operations for ACL configuration.

OLH topics: olhACL, olhACLIP, olhACLVLAN, olhACLInterface, olhACLMAC
"""
from tasks import ArubaSwitch


def list_ip_acl(sw: ArubaSwitch):
    """Return list of dicts with IPv4 ACL rules.

    OLH: olhACLIP
    Tab: IPv4 ACL Rules (#tabIPv4ACLRules)
    Table: #datagrid-ipv4acl-rules
    """
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(4000)
    sw.page.click("a[href='#tabIPv4ACLRules']")
    sw.page.wait_for_timeout(2000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-ipv4acl-rules').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_mac_acl(sw: ArubaSwitch):
    """Return list of dicts with MAC ACL rules.

    OLH: olhACLMAC
    Tab: MAC ACL Rules (#tabMACACLRules)
    Table: #datagrid-macacl-rules
    """
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(4000)
    sw.page.click("a[href='#tabMACACLRules']")
    sw.page.wait_for_timeout(2000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-macacl-rules').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_vlan_acl(sw: ArubaSwitch):
    """Return list of dicts with VLAN-bound ACLs.

    OLH: olhACLVLAN
    Tab: VLAN Configuration (#tabVLAN)
    Table: #datagrid-vlan-bound-acl
    """
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(4000)
    sw.page.click("a[href='#tabVLAN']")
    sw.page.wait_for_timeout(2000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-vlan-bound-acl').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_acl_interface_bindings(sw: ArubaSwitch):
    """Return list of dicts with interface-bound ACLs.

    OLH: olhACLInterface
    Tab: Interface Configuration (#tabInterface)
    Table: #datagrid-interface-bound-acl
    """
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(4000)
    sw.page.click("a[href='#tabInterface']")
    sw.page.wait_for_timeout(2000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-interface-bound-acl').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_acl_summary(sw: ArubaSwitch):
    """Return list of dicts with ACL summary (name, type, rule count, bound interfaces).

    OLH: olhACL
    Table: #datagrid-acl-list
    """
    sw.navigate('qos', 'acl')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-acl-list').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
