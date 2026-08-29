# Aruba Instant On 1930 Switch Management

## Overview
Two Aruba Instant On 1930 24G 4SFP/SFP+ switches (JL682A) on the management VLAN (192.168.27.0/24).

| Switch | IP | Hostname | Firmware | Location |
|--------|-----|----------|----------|----------|
| 192.168.27.2 | closet-aruba | vInstantOn_1930_3.4.0 | Closet |
| 192.168.27.3 | Livingroom-aruba | vInstantOn_1930_3.4.0 | Livingroom |

Both upgraded from 2.8.0.0 / 2.6.0.0 to 3.4.0 on 08/26/2026.

## VLAN Configuration (as of 08/26/2026)

| VLAN | Name | Purpose |
|------|------|---------|
| 1 | management | Switch management, SSH/admin |
| 2 | WAN | ISP router uplink |
| 3 | home | Home network |
| 4 | work | Work network |

VLANs 5+ are unused. (VLAN 10 was removed 08/26/2026 after first clearing the IP interface via Routing > Routing Configuration.)

## Access
- **Web GUI only** — no SSH, no CLI
- Credentials in `aruba/cred.txt` (sourceable: `aruba_user`, `aruba_pwd`)
- HTTP only (no HTTPS)
- Help accessible via `#btnTopHelp` button on every page

## Dashboard (Home page after login)
- System Information: Software Version, OS version (4.4.120), Serial Number, MAC Address
- System Resource Usage: CPU Utilization (60s avg), Memory Usage
- Device Locator LED toggle
- Configuration Wizards: Getting Started Wizard, VLAN Configuration Wizard
- REFRESH and APPLY buttons at bottom

## Navigation Structure (3.4.0)

### Setup Network (#folder_1020)
- Get Connected (#item_1020_1030)
- System Time (#item_1020_1040)
- User Management (#item_1020_1050)
- Schedule Configuration (#item_1020_1370)

### Switching (#folder_1070)
- Port Configuration (#item_1070_1080)
- Port Mirroring (#item_1070_1090)
- Loop Protection (#item_1070_1100)
- IGMP Snooping (#item_1070_1110)
- SNMP (#item_1070_1120)
- Interface Auto Recovery (#item_1070_1130)
- Trunk Configuration (#item_1070_1300)
- EEE Configuration (#item_1070_1550)

### Spanning Tree (#folder_1140)
- Global Settings (#item_1140_1150)
- CST Configuration (#item_1140_1170)
- MSTP Configuration (#item_1140_1160)

### VLAN (#folder_1200)
- VLAN Configuration (#item_1200_1210)
- Voice VLAN Configuration (#item_1200_1220)

### Neighbor Discovery (#folder_1310)
- LLDP (#item_1310_1320)
- LLDP-MED (#item_1310_1330)

### Routing (#folder_1380)
- Routing Configuration (#item_1380_1390)
- DHCP Relay (#item_1380_1410)
- ARP Table (#item_1380_1420)

### Quality of Service (#folder_1430)
- Access Control Lists (#item_1430_1440)
- Class of Service (#item_1430_1450)

### Security (#folder_1460)
- RADIUS Configuration (#item_1460_1480)
- Port Access Control (#item_1460_1490)
- Port Security (#item_1460_1500)
- Protected Ports (#item_1460_1510)
- DHCP Snooping (#item_1460_1520001)
- ARP Attack Protection (#item_1460_1530)
- Denial of Service Protection (#item_1460_1470)
- HTTPS Certificate (#item_1460_1540)

### Diagnostics (#folder_1560)
- Logging (#item_1560_1570)
- Ping (#item_1560_1580)
- Traceroute (#item_1560_1590)
- Support File (#item_1560_1610)
- Cable Test (#item_1560_1615)
- MAC Table (#item_1560_1630)
- RMON (#item_1560_1650)

### Maintenance (#folder_1660)
- Dual Image Configuration (#item_1660_1670)
- Backup and Update Files (#item_1660_1680)
- Configuration File Operations (#item_1660_1690)
- Reset (#item_1660_1600)

## Tasks API (in `aruba/tasks/`)

Reusable Python modules for switch operations. Import and use instead of raw Playwright.

### Usage
```python
import sys
sys.path.insert(0, '/home/madchaz/k3s/aruba')
from tasks import connect, disconnect
from tasks.read import list_vlans, list_ports, list_trunks, backup_config, get_firmware_info
from tasks.write import add_vlan, rename_vlan, delete_vlan, set_vlan_ip

sw = connect("192.168.27.2")  # cred_file defaults to aruba/cred.txt
# sw = connect("192.168.27.3", cred_file="/path/to/other/cred.txt")
# ... operations ...
disconnect(sw)
```

### Credential Safety
- `connect()`, `get_creds()`, and `ArubaSwitch.__init__()` all accept optional `cred_file` parameter
- No IPs or credentials are hardcoded — they must be provided at runtime
- Default credential file is `aruba/cred.txt` (key=value format: `aruba_user=...`, `aruba_pwd=...`)
- Never commit `cred.txt` — it is in `.gitignore`

### Folder Structure

```
tasks/
  __init__.py    - ArubaSwitch class, connect(), disconnect(), get_creds()
  read/          - Read-only operations (list, get info, backup)
    vlan.py      - list_vlans()
    routing.py   - list_vlan_interfaces()
    port.py      - list_ports()
    trunk.py     - list_trunks()
    backup.py    - backup_config(), get_firmware_info()
  write/         - Config-changing operations (add, rename, delete, set)
    vlan.py      - add_vlan(), rename_vlan(), delete_vlan()
    routing.py   - clear_vlan_ip(), set_vlan_ip(), add_static_route(), remove_static_route()
    port.py      - edit_port_pvid(), set_port_description()
    trunk.py     - disable_trunk(), clear_trunk_members()
    dhcp_relay.py        - add_dhcp_server(), remove_dhcp_server(), add_dhcp_interface(), remove_dhcp_interface()
    logging.py             - enable_logging(), set_log_severity(), add_remote_log_server(), remove_remote_log_server()
    loop_protection.py     - enable_loop_protection(), set_loop_protection_time(), set_port_loop_protection()
    eee_config.py          - enable_ee(), enable_low_power()
    maintenance.py         - reboot_switch()
    voice_vlan.py          - add_telephony_oui(), remove_telephony_oui(), restore_telephony_oui()
    stp_global.py          - enable_stp(), set_stp_priority(), set_stp_timers(), enable_bpdu_filter()
    mstp_config.py         - add_mstp_instance(), edit_mstp_instance(), remove_mstp_instance(), set_mstp_port_params()
    lldp.py                - set_lldp_timers(), configure_lldp_interface()
    igmp_snooping.py       - configure_igmp_snooping(), set_igmp_querier(), add_static_member()
    protected_ports.py     - enable_protected_port()
    dos_protection.py      - enable_dos_protection(), set_dos_threshold()
    arp_attack_protection.py - enable_arp_protection(), set_arp_interface_protection(), add_arp_access_rule(), remove_arp_access_rule()
    port_security.py       - enable_port_security(), add_static_mac(), remove_static_mac()
    radius.py              - add_radius_server(), edit_radius_server(), remove_radius_server()
    schedule_config.py     - add_schedule(), remove_schedule()
    dhcp_snooping.py       - enable_dhcp_snooping(), set_dhcp_trusted_port(), add_dhcp_binding(), clear_dhcp_bindings()
    port_mirroring.py      - add_mirror_session(), edit_mirror_session(), remove_mirror_session()
    snmp.py                - enable_snmp(), add_snmp_community(), remove_snmp_community(), add_snmp_trap_receiver(), remove_snmp_trap_receiver()
    acl.py                 - add_acl(), add_acl_rule_ipv4(), remove_acl_rule_ipv4(), remove_acl(), bind_acl_to_interface(), bind_acl_to_vlan()
    cos.py                 - set_cos_priority(), set_queue_scheduling(), set_traffic_type(), set_interface_shaping_rate()
    port_access_control.py - add_mac_auth_rule(), remove_mac_auth_rule(), add_mac_auth_group(), remove_mac_auth_group(), set_vlan_authentication()
    https_cert.py          - generate_certificate(), import_certificate(), delete_certificate()
```

### Available Modules

| Module | Functions | Purpose |
|--------|-----------|---------|
| `tasks` (base) | `connect(ip, cred_file)`, `disconnect(sw)`, `get_creds(cred_file)`, `ArubaSwitch(ip, page, cred_file)` | Auth, navigation, config download, OLH help |
| `tasks.read.vlan` | `list_vlans()` | VLAN list |
| `tasks.write.vlan` | `add_vlan()`, `rename_vlan()`, `delete_vlan()` | VLAN CRUD (write) |
| `tasks.read.routing` | `list_vlan_interfaces()` | VLAN IP list |
| `tasks.write.routing` | `clear_vlan_ip()`, `set_vlan_ip()` | VLAN IP management |
| `tasks.read.port` | `list_ports()` | Port list |
| `tasks.write.port` | `edit_port_pvid()`, `set_port_description()` | Port config |
| `tasks.read.trunk` | `list_trunks()` | Trunk list |
| `tasks.write.trunk` | `disable_trunk()`, `clear_trunk_members()` | Trunk management |
| `tasks.read.backup` | `backup_config()`, `get_firmware_info()` | Config backup and firmware info |
| `tasks.write.dhcp_relay` | `add_dhcp_server()`, `remove_dhcp_server()`, `add_dhcp_interface()`, `remove_dhcp_interface()` | DHCP relay config |
| `tasks.write.logging` | `enable_logging()`, `set_log_severity()`, `add_remote_log_server()`, `remove_remote_log_server()` | System logging |
| `tasks.write.loop_protection` | `enable_loop_protection()`, `set_loop_protection_time()`, `set_port_loop_protection()` | Loop protection |
| `tasks.write.eee_config` | `enable_ee()`, `enable_low_power()` | EEE energy efficient ethernet |
| `tasks.write.maintenance` | `reboot_switch()` | Switch reboot |
| `tasks.write.voice_vlan` | `add_telephony_oui()`, `remove_telephony_oui()`, `restore_telephony_oui()` | Voice VLAN OUIs |
| `tasks.write.stp_global` | `enable_stp()`, `set_stp_priority()`, `set_stp_timers()`, `enable_bpdu_filter()` | STP global settings |
| `tasks.write.mstp_config` | `add_mstp_instance()`, `edit_mstp_instance()`, `remove_mstp_instance()`, `set_mstp_port_params()` | MSTP configuration |
| `tasks.write.lldp` | `set_lldp_timers()`, `configure_lldp_interface()` | LLDP settings |
| `tasks.write.igmp_snooping` | `configure_igmp_snooping()`, `set_igmp_querier()`, `add_static_member()` | IGMP snooping |
| `tasks.write.protected_ports` | `enable_protected_port()` | Protected ports |
| `tasks.write.dos_protection` | `enable_dos_protection()`, `set_dos_threshold()` | DoS protection |
| `tasks.write.arp_attack_protection` | `enable_arp_protection()`, `set_arp_interface_protection()`, `add_arp_access_rule()`, `remove_arp_access_rule()` | ARP attack protection |
| `tasks.write.port_security` | `enable_port_security()`, `add_static_mac()`, `remove_static_mac()` | Port security |
| `tasks.write.radius` | `add_radius_server()`, `edit_radius_server()`, `remove_radius_server()` | RADIUS config |
| `tasks.write.schedule_config` | `add_schedule()`, `remove_schedule()` | Schedule config |
| `tasks.write.dhcp_snooping` | `enable_dhcp_snooping()`, `set_dhcp_trusted_port()`, `add_dhcp_binding()`, `clear_dhcp_bindings()` | DHCP snooping |
| `tasks.write.port_mirroring` | `add_mirror_session()`, `edit_mirror_session()`, `remove_mirror_session()` | Port mirroring |
| `tasks.write.snmp` | `enable_snmp()`, `add_snmp_community()`, `remove_snmp_community()`, `add_snmp_trap_receiver()`, `remove_snmp_trap_receiver()` | SNMP config |
| `tasks.write.acl` | `add_acl()`, `add_acl_rule_ipv4()`, `remove_acl_rule_ipv4()`, `remove_acl()`, `bind_acl_to_interface()`, `bind_acl_to_vlan()` | ACL management |
| `tasks.write.cos` | `set_cos_priority()`, `set_queue_scheduling()`, `set_traffic_type()`, `set_interface_shaping_rate()` | Class of service |
| `tasks.write.port_access_control` | `add_mac_auth_rule()`, `remove_mac_auth_rule()`, `add_mac_auth_group()`, `remove_mac_auth_group()`, `set_vlan_authentication()` | Port access control |
| `tasks.write.https_cert` | `generate_certificate()`, `import_certificate()`, `delete_certificate()` | HTTPS certificates |


### Navigation
`sw.navigate(folder, item)` uses keys from `ArubaSwitch.FOLDER_MAP` and `ITEM_MAP`:
- Folders: `setup`, `switching`, `spanning_tree`, `vlan`, `neighbor_discovery`, `routing`, `qos`, `security`, `diagnostics`, `maintenance`
- Items: see `ITEM_MAP` in `tasks/__init__.py` (e.g. `port_config`, `vlan_config`, `trunk_config`)

### Important Details
- Navigation: clicking a folder item collapses the folder. The `navigate()` method handles this by checking item visibility before clicking.
- DataTables: pagination and search are unreliable on 3.4.0. Use raw row iteration instead.
- Table IDs differ by page: `#datagrid-configuration` (VLAN), `#datagrid-trunks` (Trunk), `#datagrid-interface-port` (Port), `#datagrid-routing-vlan` (Routing)
- Trunk removal: web UI does NOT support removing trunks. Use `disable_trunk()` + `clear_trunk_members()` instead.
- `apply_pending()`: click page-level `#btnApply` if pending changes exist (returns True if clicked)
- `close_any_modal()`: closes open modal dialogs to prevent blocking navigation

## Legacy Automation Scripts (in `aruba/`)

### backup.py
Downloads running config from both switches. Uses reverse-engineered web API:
1. GET `/` → extract dynamic document root from redirect
2. GET `/device/wcd?{EncryptionSetting}` → RSA public key + login token
3. RSA-encrypt credentials, GET `system.xml?action=login&cred=<hex>`
4. GET `authenticate_user.xml` → authenticated session
5. GET `http_download?action=2&ssd=4` → full config text

Saves as `<hostname>.cfg` in `aruba/`. Requires `requests` + `pycryptodome`.

### vlan_rename.py / vlan_delete.py
Legacy Playwright scripts (superseded by `aruba/tasks/vlan.py`). VLAN 1 (Default) checkbox is always disabled.

## Web UI Navigation (Playwright selectors)
- VLAN folder: `a[href='#folder_1200']`
- VLAN Configuration: `a[href='#item_1200_1210']`
- Edit button: `#vlan-edit-conf`
- Remove button: `#vlan-remove-conf`
- Add button: `#vlan-add-conf`
- Refresh: `#vlan-refresh-conf`
- Page-level Apply: `#btnApply` (appears when pending changes exist)
- Edit modal: `#modalEditVlan` with `#txtEditVlanName`
- Add modal: `#modalAddVlan` with `#txtAddVlanId`, `#txtAddVlanName`

### Routing page selectors
- Routing Configuration: `a[href='#item_1380_1390']`
- Routing VLAN table: `#datagrid-routing-vlan`
- Edit button: `#routing-edit-vlan`
- Refresh button: `#routing-refresh-vlan`
- Modal: `.modal.show`
- IP method radio buttons: `#rbVlanIPAddressMethod_0` (None), `_1` (Manual), `_2` (DHCP)
- IP address field: `#txtVlanIPAddress`
- Subnet mask field: `#txtVlanSubnetMask`
- Modal Apply: button with text "APPLY"

### Trunk page selectors
- Trunk Configuration: `a[href='#item_1070_1300']`
- Trunk table: `#datagrid-trunks`
- Edit button: `#trunks-edit`
- Refresh button: `#trunks-refresh`
- Columns: 0=checkbox, 1=Trunk name, 2=Description, 3=Type, 4=Admin Mode, 5=Link Status, 6=Members, 7=Active Ports, 8=actions
- Modal: `.modal.show` with `#chkAdminMode` (enable/disable), `#txtDescription`, `#multiselect` (available ports), `#multiselect2` (selected ports), `#multiselect_rightSelected`/`#multiselect_leftSelected` buttons
- **No remove button exists** — trunks can only be disabled and have ports removed

### Port page selectors
- Port Configuration: `a[href='#item_1070_1080']`
- Port table: `#datagrid-interface-port`
- Edit button: `#edit-interface`
- Columns: 0=checkbox, 1=Interface, 2=Description, 3=Type, 4=Admin Mode, 5=Schedule, 6=Physical Mode, 7=Physical Status, 8=Auto Negotiation, 9=STP Mode, 10=LACP Mode, 11=Link Status
- Modal: `.modal.show` with `#modalEditButtonApply`, `#modalEditButtonCancel`

## Config Download via JS
```js
fetch(window.location.origin + '/hpe/http_download?action=2&ssd=4', {
    credentials: 'include'
}).then(r => r.text());
```

## Firmware Upgrade
- **Current**: Both switches on 3.4.0 (upgraded 08/26/2026)
- Firmware file: `InstantOn_1930_3.4.0.6.swi` (37MB) in `aruba/`
- Latest version page: https://community.instant-on.hpe.com/viewdocument/1930-software
- Upgrade via web UI: Maintenance > Backup and Update Files
- **CRITICAL**: Always backup config before upgrade
- Upgrades require a reboot
- Release notes PDFs in `aruba/rn_1930_*.pdf` (HPE's download page blocks direct fetch with 403)
- **VLAN 1 trunk issue**: Firmware upgrades can remove VLAN 1 from trunk allowed VLAN list. If this happens, re-add VLAN 1 to TRK1 on both switches via VLAN > VLAN Configuration.

## Online Help (OLH)

Every logged-in page embeds help content as CDATA in `<script id="olh...">` tags. Help is loaded **globally** on every page — no navigation required to access any topic.

### Usage
```python
from tasks import connect, disconnect
sw = connect("192.168.27.2")  # or with explicit cred_file
# Get all help topics
topics = sw.list_help_topics()
# Get help for specific topic (case-insensitive match on id or content)
help_html = sw.get_help("SNMPSetting")
help_html = sw.get_help("vlan")  # matches olhVLAN, olhVLANConfiguration, etc.
# Get everything
all_help = sw.get_help()
disconnect(sw)
```

### Help Topic IDs (selected)
| ID | Topic |
|----|-------|
| `olhSNMPSetting` | SNMP global config |
| `olhCommunityConfiguration` | SNMP community strings |
| `olhVLANConfiguration` | VLAN config |
| `olhPortConfiguration` | Port config |
| `olhTrunkConfiguration` | Trunk config |
| `olhRoutingGlobal` | Routing |
| `olhSuspendedInterfaces` | Suspended interfaces |
| `olhLoopProtection` | Loop protection |

**IMPORTANT**: When debugging or implementing a new feature, **check the switch help section FIRST** using `sw.get_help(topic)` before guessing at UI behavior. The OLH contains step-by-step instructions from HPE for every page.

## SNMP Exporter (Prometheus Metrics)

snmp_exporter v0.26.0 deployed in `monitoring` namespace. Scrapes both switches every 60s via Prometheus `additionalScrapeConfigs` in `monitoring-values.yaml` (job `aruba-switches`).

### Config Files
- `snmp-exporter/snmp.yml`: snmp_exporter config (auths + modules with metric definitions)
- `snmp-exporter/configmap.yaml`: K8s ConfigMap (auto-generated from snmp.yml)
- `snmp-exporter/deployment.yaml`: K8s Deployment
- `monitoring-values.yaml`: Prometheus scrape job with relabeling for per-target scraping
- `aruba-switches-dashboard.json`: Grafana dashboard source

### Grafana Dashboard
- **Aruba Switches**: http://192.168.33.200/d/aruba-switches/aruba-switches (uid: `aruba-switches`)
- Switch uptime, system info table, interface status (admin/oper, speed, MTU)
- Per-port traffic received/transmitted, TRK1 trunk traffic
- Error/discard rates, packet rates, SNMP availability

### Key Metrics
- `sysName`, `sysDescr`, `sysUpTime`: system info
- `ifAdminStatus`, `ifOperStatus`: interface up/down
- `ifHCInOctets`, `ifHCOutOctets`: high-precision traffic counters
- `ifInErrors`, `ifOutErrors`, `ifInDiscards`, `ifOutDiscards`: error/discard counters
- `ifSpeed`, `ifMtu`: interface properties
- Labels: `instance` (switch IP), `ifIndex`, `ifDescr`, `ifName`

### Gotchas
- snmp_exporter v0.26.0 requires lowercase index types (`gauge` not `Gauge32`)
- Each SNMP target needs separate scrape request (no multi-target support)
- ConfigMap must be recreated (not patched) when snmp.yml changes significantly
- Community string `YOUR_COMMUNITY_STRING`, SNMP v2c, auth key `aruba_auth`
- No SSH/API — all operations through web GUI
- Config download works but config upload does NOT work
- VLAN deletion blocked if IP interface or DHCP relay exists on VLAN
- Trunk between switches (TRK1, port 28) carries VLANs 1-4 tagged
- SNMP read-only community `YOUR_COMMUNITY_STRING` allows 0.0.0.0 (updated 08/26/2026)
- Help button (`#btnTopHelp`) navigates to Dashboard page, not a help document — use OLH API instead

## Function Index

### Base (`tasks/__init__.py`)
| Function | OLH Topics |
|----------|-----------|
| `connect(ip, cred_file)` | n/a |
| `disconnect(sw)` | n/a |
| `get_creds(cred_file)` | n/a |
| `ArubaSwitch.navigate(folder, item)` | all |
| `ArubaSwitch.apply_pending()` | n/a |
| `ArubaSwitch.close_any_modal()` | n/a |
| `ArubaSwitch.download_config()` | olhBackup |
| `ArubaSwitch.get_firmware_version()` | olhMaintenance |
| `ArubaSwitch.get_help(topic)` | all |
| `ArubaSwitch.list_help_topics()` | all |

### Read Modules (`tasks/read/`)
| Module | Function | OLH Topics |
|--------|----------|-----------|
| vlan | `list_vlans()` | olhVLAN, olhVLANConfiguration |
| vlan | `get_vlan_device_view()` | olhVLANDeviceView |
| routing | `list_vlan_interfaces()` | olhRouting, olhRoutingPortVlan |
| routing | `get_vlan_interface_configuration()` | olhVLANInterfaceConfiguration |
| port | `list_ports()` | olhPortConfiguration, olhPortConfigurationDeviceView |
| trunk | `list_trunks()` | olhTrunkConfiguration, olhTrunkGlobal |
| backup | `backup_config()` | olhBackup, olhConfigurationFile |
| backup | `get_firmware_info()` | olhMaintenance |
| backup | `get_firmware_info()` | olhMaintenance |
| acl | `list_ip_acl()` | olhACL, olhACLIP |
| acl | `list_mac_acl()` | olhACLMAC |
| acl | `list_vlan_acl()` | olhACLVLAN |
| acl | `list_acl_interface_bindings()` | olhACLInterface |
| acl | `list_acl_summary()` | olhACL |
| arp | `list_arp_table()` | olhARP, olhARPTable, olhARPGlobal |
| arp | `get_arp_attack_protection()` | olhARPAttackProtection, olhARPAttackProtectionGlobal |
| arp | `get_arp_protection_per_interface()` | olhARPAttackProtectionInterface |
| arp | `get_arp_protection_per_vlan()` | olhARPAttackProtectionVlan |
| arp | `get_arp_access_control_rules()` | olhARPAttackProtectionACL |
| cos | `get_cos_general_settings()` | olhQoS, olhCoS, olhCoSGeneral |
| cos | `list_priority_map()` | olhCoSPriority |
| cos | `list_queue_config()` | olhCoSQueue |
| cos | `list_dscp_cos_map()` | olhCoSDSCP |
| cos | `list_cos_statistics()` | olhCoSStatistics |
| cos | `list_interface_cos_config()` | olhCoSShaping |
| cos | `get_cos_shaping()` | olhCoSShaping |
| cst | `get_cst_status()` | olhCST |
| cst | `get_cst_config()` | olhCSTConfiguration |
| dhcp | `get_dhcp_relay_global()` | olhDHCPRelay, olhDHCPRelayGlobal |
| dhcp | `list_dhcp_relay_servers()` | olhDHCPRelayServer |
| dhcp | `list_dhcp_relay_interfaces()` | olhDHCPRelayInterfaces |
| dhcp | `get_dhcp_snooping_status()` | olhDHCPSnooping, olhDHCPSnoopingGlobal |
| dhcp | `list_dhcp_bindings()` | olhDHCPBindingDatabase |
| dhcp | `get_dhcp_interface_settings()` | olhDHCPInterfaceSettings |
| dhcp | `get_dhcp_vlan_settings()` | olhDHCPVLANSettings |
| dsp | `get_dos_protection_status()` | olhDSP, olhDSPGlobal |
| dsp | `get_dsp_per_interface()` | olhDSPInterface |
| dsp | `get_syn_attack_status()` | olhDSPSynAttack |
| eee | `get_eee_global_status()` | olhEEE, olhEEEGlobal, olhEEEGlobalStatus |
| eee | `get_eee_per_interface()` | olhEEEInterfaceStatus |
| igmp | `get_igmp_snooping_status()` | olhIGMP, olhIGMPSnooping |
| igmp | `get_igmp_forwarding()` | olhIGMPSnoopingForwarding |
| igmp | `list_igmp_multicast()` | olhIGMPSnoopingMulticast |
| igmp | `get_igmp_per_vlan()` | olhIGMPSnoopingVLAN |
| igmp | `get_igmp_unregistered_multicast()` | olhIGMPSnoopingUnregisteredMulticast |
| lag | `list_lag_groups()` | olhLAG, olhLAGDeviceView |
| lldp | `get_lldp_global()` | olhLLDP, olhLLDPGlobal |
| lldp | `get_lldp_per_interface()` | olhLLDPInterface |
| lldp | `list_lldp_neighbors()` | olhLLDPLocalDevice, olhLLDPRemotelDevice |
| lldp | `get_lldp_stats()` | olhLLDPStatistics |
| lldp | `get_lldp_information()` | olhLLDPInformation |
| lldp_med | `get_lldpmed_global()` | olhLLDPMED, olhLLDPMEDConfiguration |
| lldp_med | `get_lldpmed_information()` | olhLLDPMEDInformation |
| lldp_med | `get_lldpmed_per_interface()` | olhLLDPMEDInterface |
| lldp_med | `list_lldpmed_remote_devices()` | olhLLDPMEDRemote |
| logging | `get_log_global_config()` | olhLoggingGlobal |
| logging | `list_buffered_logs()` | olhLoggingBufferedLog |
| logging | `list_log_messages()` | olhLoggingMessage |
| logging | `get_remote_log_config()` | olhLoggingRemoteLog |
| logging | `get_log_file()` | olhLoggingLogFile |
| loop_protection | `get_loop_protection_status()` | olhLoopProtection, olhLoopProtectionOverview |
| loop_protection | `get_loop_protection_per_interface()` | olhLoopProtectionInterfaces |
| mac | `list_mac_table()` | olhMACTable, olhMACAddressTable |
| mac | `get_mac_table_global()` | olhMACTableGlobal |
| mstp | `get_mstp_config()` | olhMSTP, olhMSTPConfiguration |
| mstp | `get_mstp_per_port()` | olhMSTPPortConfiguration |
| poe | `list_poe_ports()` | olhPOE, olhPOEDeviceView, olhPOEPortConfiguration |
| poe | `get_poe_schedule()` | olhPOESchedule, olhPOEScheduleConfiguration |
| poe | `get_poe_consumption_history()` | olhPOEConsumptionHistory |
| poe | `get_poe_status()` | olhPOEStatus |
| radius | `list_radius_servers()` | olhRadiusServer |
| radius | `get_radius_global()` | olhRadiusGlobal |
| rmon | `get_rmon_global()` | olhRMON |
| rmon | `list_rmon_alarms()` | olhRMONAlarms |
| rmon | `list_rmon_collectors()` | olhRMONCollectors |
| rmon | `list_rmon_events()` | olhRMONEventLog, olhRMONEvents |
| rmon | `list_rmon_statistics()` | olhRMONStatistics, olhRMONHistoryLog |
| snmp | `get_snmp_settings()` | olhSNMP, olhSNMPSetting |
| snmp | `list_snmp_communities()` | olhCommunityConfiguration |
| snmp | `list_snmp_users()` | olhSNMPUser |
| snmp | `get_snmp_v3_receivers()` | olhReceiversV3 |
| snmp | `get_snmp_engine_id()` | olhSNMPEngineId |
| snmp | `list_snmp_filters()` | olhSNMPFilter |
| snmp | `list_snmp_views()` | olhSNMPView |
| snmp | `get_snmp_v1v2_receivers()` | olhReceiversV1V2 |
| stp | `get_stp_global_status()` | olhSTP, olhSTPGlobal, olhSTPGlobalSettings |
| stp | `get_stp_statistics()` | olhSpanningTreeStatistis |
| voice_vlan | `get_voice_vlan_global()` | olhVoiceVLAN, olhVoiceVLANGlobal |
| voice_vlan | `get_voice_vlan_per_interface()` | olhVoiceVLANInterface |
| voice_vlan | `list_voice_vlan_ouis()` | olhVoiceVLANOUI |
| interface | `get_interface_config()` | olhInterfaceConfiguration |
| interface | `get_auto_recovery_settings()` | olhInterfaceAutoRecovery, olhInterfaceRecoverySetting |
| system | `get_system_info()` | olhSystemInformation |
| system | `get_system_time()` | olhSystemTime, olhSystemTimeSetup, olhTimeConfiguration |
| system | `get_system_resources()` | olhSystemResource |
| system | `list_user_accounts()` | olhUserAccounts, olhUserManagement |
| system | `get_password_rules()` | olhAccountSecuritySettings, olhPasswordRules |
| system | `list_user_sessions()` | olhUserSessions |
| system | `get_management_vlan()` | olhManagementVLANSettings |
| system | `get_daylight_saving()` | olhDaylightSaving |
| system | `get_logged_in_sessions()` | olhLoggedIn |
| system | `list_password_keywords()` | olhKeywords |
| system | `get_dashboard_info()` | olhDashboard |
| system | `get_dashboard_device_view()` | olhDashboardDeviceView |
| system | `get_device_information()` | olhDeviceInformation |
| diagnostics | `ping()` | olhPing, olhPing4, olhPing6, olhPingResult, olhDiagnostics |
| diagnostics | `traceroute()` | olhTraceroute, olhTraceroute4, olhTraceroute6, olhTracerouteResult |
| diagnostics | `cable_test()` | olhCableTest, olhCableTestInterfaceConfiguration |
| diagnostics | `download_support_file()` | olhSupportFile |
| security | `list_port_security()` | olhSecurity, olhPortSecurity, olhPortSecurityConfiguration, olhPortSecurityDynamicMac, olhPortSecurityStaticMac |
| security | `get_port_access_control()` | olhPortAccessControl, olhPortAccessControlPort |
| security | `get_port_access_control_global()` | olhPortAccessControlGlobal |
| security | `list_port_access_control_vlan()` | olhPortAccessControlVlan |
| security | `list_port_access_control_supplicant()` | olhPortAccessControlSupplicant |
| security | `list_port_access_control_client()` | olhPortAccessControlClient |
| security | `get_port_access_control_statistics()` | olhPortAccessControlStatistics |
| security | `list_port_access_control_mac()` | olhPortAccessControlMac |
| security | `list_protected_ports()` | olhProtectedPorts, olhProtectedPortsInterfaces |
| security | `get_port_access_control()` | olhAccessControlGroup |
| port_stats | `get_port_statistics()` | olhPortStatistics, olhPortInformation |
| port_stats | `list_suspended_interfaces()` | olhSuspendedInterfaces |
| port_mirroring | `list_mirroring_sessions()` | olhPortMirroring, olhMirroringSessions |
| routing_stats | `get_routing_global()` | olhRoutingGlobal |
| routing_stats | `list_route_table()` | olhRoutingRouteTable |
| routing_stats | `list_static_routes()` | olhRoutingStaticRouting |
| routing_stats | `get_routing_stats()` | olhRoutingICMPStatistics, olhRoutingIPStatistics |
| vlan_membership | `list_vlan_membership_by_interface()` | olhVLANMembershipByInterface |
| vlan_membership | `list_vlan_membership_by_vlan()` | olhVLANMembershipByVLAN |
| device_locator | `get_device_locator_status()` | olhDeviceLocator |
| http_https | `get_http_settings()` | olhHTTPManagementSettings |
| http_https | `get_https_settings()` | olhHTTPS |
| http_https | `get_certificate_info()` | olhHTTPSCertificate |
| ipv6 | `get_ipv6_setup()` | olhIPv6Setup |
| get_connected | `get_ipv4_setup()` | olhIPv4Setup |
| get_connected | `get_network_setup()` | olhGetConnected |
| maintenance | `get_config_file_info()` | olhConfigurationFile |
| maintenance | `get_reboot_status()` | olhRebootDevice |
| maintenance | `get_reset_status()` | olhReset |
| maintenance | `get_reset_defaults_status()` | olhResetDefaults |
| maintenance | `get_config_wizard_status()` | olhConfigWizard |

### Write Modules (`tasks/write/`)
| Module | Function | OLH Topics |
|--------|----------|-----------|
| vlan | `add_vlan(vid, name)` | olhVLANConfiguration |
| vlan | `rename_vlan(vid, new_name)` | olhVLANConfiguration |
| vlan | `delete_vlan(vid)` | olhVLANConfiguration |
| routing | `clear_vlan_ip(vid)` | olhRoutingPortVlan |
| routing | `set_vlan_ip(vid, ip, mask)` | olhRoutingPortVlan |
| port | `edit_port_pvid(port, pvid)` | olhPortConfiguration |
| port | `set_port_description(port, desc)` | olhPortConfiguration |
| trunk | `disable_trunk(trunk_num)` | olhTrunkConfiguration |
| trunk | `clear_trunk_members(trunk_num)` | olhTrunkConfiguration |
| routing | `add_static_route(destination, mask, gateway, vid)` | olhRoutingStaticRouting |
| routing | `remove_static_route(idx)` | olhRoutingStaticRouting |
| dhcp_relay | `add_dhcp_server(ip)` | olhDHCPRelay, olhDHCPRelayServer |
| dhcp_relay | `remove_dhcp_server(ip)` | olhDHCPRelay, olhDHCPRelayServer |
| dhcp_relay | `add_dhcp_interface(vid)` | olhDHCPRelayInterfaces |
| dhcp_relay | `remove_dhcp_interface(vid)` | olhDHCPRelayInterfaces |
| logging | `enable_logging()` | olhLoggingGlobal |
| logging | `set_log_severity(severity)` | olhLoggingGlobal |
| logging | `add_remote_log_server(ip, port)` | olhLoggingRemoteLog |
| logging | `remove_remote_log_server(idx)` | olhLoggingRemoteLog |
| loop_protection | `enable_loop_protection()` | olhLoopProtection |
| loop_protection | `set_loop_protection_time(seconds)` | olhLoopProtection |
| loop_protection | `set_port_loop_protection(port, enable)` | olhLoopProtectionInterfaces |
| eee_config | `enable_ee()` | olhEEE, olhEEEGlobal |
| eee_config | `enable_low_power()` | olhEEE, olhEEEGlobal |
| maintenance | `reboot_switch()` | olhMaintenance, olhRebootDevice |
| voice_vlan | `add_telephony_oui(oui)` | olhVoiceVLAN, olhVoiceVLANOUI |
| voice_vlan | `remove_telephony_oui(oui)` | olhVoiceVLAN, olhVoiceVLANOUI |
| voice_vlan | `restore_telephony_oui()` | olhVoiceVLAN, olhVoiceVLANOUI |
| stp_global | `enable_stp()` | olhSTP, olhSTPGlobal |
| stp_global | `set_stp_priority(priority)` | olhSTP, olhSTPGlobal |
| stp_global | `set_stp_timers(fwd_delay, hello_time, max_age)` | olhSTP, olhSTPGlobal |
| stp_global | `enable_bpdu_filter()` | olhSTP, olhSTPGlobal |
| mstp_config | `add_mstp_instance(revision, name)` | olhMSTP, olhMSTPConfiguration |
| mstp_config | `edit_mstp_instance(idx, revision, name)` | olhMSTP, olhMSTPConfiguration |
| mstp_config | `remove_mstp_instance(idx)` | olhMSTP, olhMSTPConfiguration |
| mstp_config | `set_mstp_port_params(port, instance, priority, weight)` | olhMSTPPortConfiguration |
| lldp | `set_lldp_timers(tx_interval, tx_count, hold_time)` | olhLLDP, olhLLDPGlobal |
| lldp | `configure_lldp_interface(port, tx, rx)` | olhLLDPInterface |
| igmp_snooping | `configure_igmp_snooping(vid, enable, fast_leave)` | olhIGMP, olhIGMPSnooping |
| igmp_snooping | `set_igmp_querier(vid, enable, ip)` | olhIGMPSnooping |
| igmp_snooping | `add_static_member(vid, port, group)` | olhIGMPSnoopingMulticast |
| protected_ports | `enable_protected_port(port)` | olhProtectedPorts |
| dos_protection | `enable_dos_protection()` | olhDSP, olhDSPGlobal |
| dos_protection | `set_dos_threshold(rate)` | olhDSP, olhDSPGlobal |
| arp_attack_protection | `enable_arp_protection()` | olhARPAttackProtection |
| arp_attack_protection | `set_arp_interface_protection(port, enable)` | olhARPAttackProtectionInterface |
| arp_attack_protection | `add_arp_access_rule(vid, mac, ip)` | olhARPAttackProtectionACL |
| arp_attack_protection | `remove_arp_access_rule(idx)` | olhARPAttackProtectionACL |
| port_security | `enable_port_security()` | olhPortSecurity |
| port_security | `add_static_mac(port, mac)` | olhPortSecurityStaticMac |
| port_security | `remove_static_mac(idx)` | olhPortSecurityStaticMac |
| radius | `add_radius_server(ip, port, secret)` | olhRadiusServer |
| radius | `edit_radius_server(idx, ip, port, secret)` | olhRadiusServer |
| radius | `remove_radius_server(idx)` | olhRadiusServer |
| schedule_config | `add_schedule(name, type, value)` | olhSchedule, olhScheduleConfiguration |
| schedule_config | `remove_schedule(idx)` | olhSchedule, olhScheduleConfiguration |
| dhcp_snooping | `enable_dhcp_snooping()` | olhDHCPSnooping |
| dhcp_snooping | `set_dhcp_trusted_port(port, trusted)` | olhDHCPSnooping |
| dhcp_snooping | `add_dhcp_binding(mac, ip, vid, port)` | olhDHCPBindingDatabase |
| dhcp_snooping | `clear_dhcp_bindings()` | olhDHCPBindingDatabase |
| port_mirroring | `add_mirror_session(name, source, direction, dest)` | olhPortMirroring |
| port_mirroring | `edit_mirror_session(idx, name, source, direction, dest)` | olhPortMirroring |
| port_mirroring | `remove_mirror_session(idx)` | olhPortMirroring |
| snmp | `enable_snmp()` | olhSNMP, olhSNMPSetting |
| snmp | `add_snmp_community(name, access, ip)` | olhCommunityConfiguration |
| snmp | `remove_snmp_community(idx)` | olhCommunityConfiguration |
| snmp | `add_snmp_trap_receiver(name, ip, community)` | olhReceiversV1V2 |
| snmp | `remove_snmp_trap_receiver(idx)` | olhReceiversV1V2 |
| acl | `add_acl(name)` | olhACL, olhACLIP |
| acl | `add_acl_rule_ipv4(idx, rule)` | olhACL, olhACLIP |
| acl | `remove_acl_rule_ipv4(idx, rule_idx)` | olhACL, olhACLIP |
| acl | `remove_acl(idx)` | olhACL, olhACLIP |
| acl | `bind_acl_to_interface(acl_idx, port, direction)` | olhACLInterface |
| acl | `bind_acl_to_vlan(acl_idx, vid, direction)` | olhACLVLAN |
| cos | `set_cos_priority(mapping)` | olhCoS, olhCoSPriority |
| cos | `set_queue_scheduling(queue, type, weight)` | olhCoSQueue |
| cos | `set_traffic_type(mapping)` | olhCoS |
| cos | `set_interface_shaping_rate(port, rate)` | olhCoSShaping |
| port_access_control | `add_mac_auth_rule(name, action)` | olhPortAccessControl |
| port_access_control | `remove_mac_auth_rule(idx)` | olhPortAccessControl |
| port_access_control | `add_mac_auth_group(name, rule_idx)` | olhAccessControlGroup |
| port_access_control | `remove_mac_auth_group(idx)` | olhAccessControlGroup |
| port_access_control | `set_vlan_authentication(vid, vlan)` | olhPortAccessControlVlan |
| https_cert | `generate_certificate(cn, key_size, validity)` | olhHTTPSCertificate |
| https_cert | `import_certificate(cert_path, key_path)` | olhHTTPSCertificate |
| https_cert | `delete_certificate(idx)` | olhHTTPSCertificate |

## AI Attribution

This work was generated by a human-guided AI assistant. The model is Qwen3.6-27B-Q4 (pooled/qwen3.6-27b-q4), hosted locally on three NVIDIA GPUs (1x GeForce RTX 3060, 2x GeForce GTX 1080 Ti). No cloud APIs were used.
