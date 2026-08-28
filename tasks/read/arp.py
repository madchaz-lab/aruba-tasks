"""Read operations for ARP configuration.

OLH topics: olhARP, olhARPTable, olhARPGlobal, olhARPAttackProtection,
            olhARPAttackProtectionGlobal, olhARPAttackProtectionInterface,
            olhARPAttackProtectionVlan, olhARPAttackProtectionACL
"""
from tasks import ArubaSwitch


def list_arp_table(sw: ArubaSwitch):
    """Return list of dicts with ARP table entries.

    OLH: olhARPTable, olhARPGlobal
    Table: #datagrid-arp
    """
    sw.navigate('routing', 'arp_table')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-arp').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_arp_attack_protection(sw: ArubaSwitch):
    """Return dict with ARP attack protection global settings.

    OLH: olhARPAttackProtection, olhARPAttackProtectionGlobal
    """
    sw.navigate('security', 'arp_attack_protection')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = {};

            // Check ARP Header Validation checkbox
            const headerValidation = document.querySelector('#chkARPHeaderValidation');
            if (headerValidation) {
                result.header_validation = headerValidation.checked;
            }

            // Check ARP Protection Logging checkbox
            const logging = document.querySelector('#chkARPProtectionLogging');
            if (logging) {
                result.logging_enabled = logging.checked;
            }

            // Get logging interval
            const interval = document.querySelector('#txtARPProtectionLoggingInterval');
            if (interval) {
                result.logging_interval = interval.value;
            }

            return result;
        }
    """)


def get_arp_protection_per_interface(sw: ArubaSwitch):
    """Return list of dicts with per-interface ARP attack protection settings.

    OLH: olhARPAttackProtectionInterface
    Table: #ARPInterfaceSettingsTable
    """
    sw.navigate('security', 'arp_attack_protection')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const rows = document.querySelectorAll('#ARPInterfaceSettingsTable tbody tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 2) {
                    result.push({
                        interface: cells[1].innerText.trim(),
                        trust_mode: cells[2].innerText.trim()
                    });
                }
            });
            return result;
        }
    """)


def get_arp_protection_per_vlan(sw: ArubaSwitch):
    """Return list of dicts with per-VLAN ARP attack protection settings.

    OLH: olhARPAttackProtectionVlan
    Table: #ARPVLANSettingsTable
    """
    sw.navigate('security', 'arp_attack_protection')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const rows = document.querySelectorAll('#ARPVLANSettingsTable tbody tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 3) {
                    result.push({
                        vlan_id: cells[1].innerText.trim(),
                        protection_enabled: cells[2].innerText.trim(),
                        acl_list: cells[3].innerText.trim()
                    });
                }
            });
            return result;
        }
    """)


def get_arp_access_control_rules(sw: ArubaSwitch):
    """Return list of dicts with ARP access control rules.

    OLH: olhARPAttackProtectionACL
    Table: #ARPAccessControlRulesTable
    """
    sw.navigate('security', 'arp_attack_protection')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const rows = document.querySelectorAll('#ARPAccessControlRulesTable tbody tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 3) {
                    result.push({
                        list_name: cells[1].innerText.trim(),
                        ip_address: cells[2].innerText.trim(),
                        mac_address: cells[3].innerText.trim()
                    });
                }
            });
            return result;
        }
    """)
