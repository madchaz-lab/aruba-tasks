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
from tasks import vlan, routing, port, trunk, backup

sw = connect("192.168.27.2")  # or 192.168.27.3
# ... operations ...
disconnect(sw)
```

### Available Modules

| Module | Functions | Purpose |
|--------|-----------|---------|
| `tasks` (base) | `connect()`, `disconnect()`, `ArubaSwitch.navigate()`, `apply_pending()`, `download_config()`, `get_firmware_version()`, `get_help()`, `list_help_topics()` | Auth, navigation, config download, OLH help |
| `vlan` | `list_vlans()`, `rename_vlan()`, `delete_vlan()`, `add_vlan()` | VLAN CRUD |
| `routing` | `list_vlan_interfaces()`, `clear_vlan_ip()`, `set_vlan_ip()` | VLAN IP interface management |
| `port` | `list_ports()`, `edit_port_pvid()`, `set_port_description()` | Port configuration |
| `trunk` | `list_trunks()`, `disable_trunk()`, `clear_trunk_members()` | Trunk management |
| `backup` | `backup_config()`, `get_firmware_info()` | Config backup and firmware info |


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
sw = connect("192.168.27.2")
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

## AI Attribution

This work was generated by a human-guided AI assistant. The model is Qwen3.6-27B-Q4 (pooled/qwen3.6-27b-q4), hosted locally on a NVIDIA GeForce RTX 3060 on Goku (workstation). No cloud APIs were used.
