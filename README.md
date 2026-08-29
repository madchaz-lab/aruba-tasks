# Aruba Instant On 1930 Switch Automation API

Reusable Python module for automating [Aruba Instant On 1930](https://www.arubanetworks.com/products/instant-on-switches/1930-series/) switches (JL682A) via Playwright browser automation. These switches only support web GUI management (no SSH, no CLI, no REST API).

## Dependencies

| Package | Version | Install |
|---------|---------|---------|
| Python | >= 3.10 | system |
| playwright | latest | `pip install playwright && playwright install chromium` |

## Architecture

The `tasks/` package provides:

- **`tasks`** (`__init__.py`): Base `ArubaSwitch` class with auth, navigation, config download, and OLH help extraction. Factory functions `connect()`/`disconnect()` for browser lifecycle.
- **`vlan`**: VLAN CRUD — list, rename, delete, add. Uses DataTables API on `#datagrid-configuration`.
- **`routing`**: VLAN IP interface management — list, clear, set static IP, add/remove static routes. Uses `#datagrid-routing-vlan`.
- **`port`**: Port configuration — list, set PVID, set description. Uses `#datagrid-interface-port`.
- **`trunk`**: Trunk management — list, disable, clear members. Uses `#datagrid-trunks`. Note: web UI does NOT support trunk removal.
- **`backup`**: Config download and firmware info extraction.
- **`dhcp_relay`**: DHCP relay server and interface configuration.
- **`logging`**: System logging, severity levels, and remote log servers.
- **`loop_protection`**: Global and per-port loop protection settings.
- **`eee_config`**: Energy Efficient Ethernet configuration.
- **`maintenance`**: Switch reboot operations.
- **`voice_vlan`**: Voice VLAN telephony OUI management.
- **`stp_global`**: Global STP settings, priority, timers, BPDU filter.
- **`mstp_config`**: MSTP instance and port parameter configuration.
- **`lldp`**: LLDP timer and per-interface configuration.
- **`igmp_snooping`**: IGMP snooping, querier, and static member configuration.
- **`protected_ports`**: Per-port protected port enablement.
- **`dos_protection`**: Global DoS protection and threshold settings.
- **`arp_attack_protection`**: ARP attack protection with per-interface and ACL rules.
- **`port_security`**: Port security with static MAC management.
- **`radius`**: RADIUS server CRUD operations.
- **`schedule_config`**: Schedule configuration CRUD.
- **`dhcp_snooping`**: DHCP snooping, trusted ports, and binding management.
- **`port_mirroring`**: Mirror session CRUD operations.
- **`snmp`**: SNMP enablement, community strings, and trap receivers.
- **`acl`**: ACL CRUD with IPv4 rules and interface/VLAN bindings.
- **`cos`**: Class of service priority, queue scheduling, traffic type, and shaping.
- **`port_access_control`**: MAC authentication rules, groups, and VLAN authentication.
- **`https_cert`**: HTTPS certificate generation, import, and deletion.

## Usage

```python
from tasks import connect, disconnect
from tasks import vlan, routing, port, trunk, backup
from tasks.write import stp_global, snmp, acl

sw = connect("192.168.27.2")  # switch IP
try:
    # List VLANs
    vlans = vlan.list_vlans(sw)

    # Rename VLAN
    vlan.rename_vlan(sw, 3, "home")

    # Set port PVID
    port.edit_port_pvid(sw, 1, 3)

    # Enable STP
    stp_global.enable_stp(sw)

    # Add SNMP community
    snmp.add_snmp_community(sw, "readonly", "ro", "0.0.0.0")

    # Backup config
    backup.backup_config(sw, "/path/to/backup.cfg")
finally:
    disconnect(sw)
```

### Custom credentials file

```python
sw = connect("192.168.27.2", cred_file="/path/to/creds.txt")
```

Credentials file format (key=value, `#` comments):
```
aruba_user=your_username
aruba_pwd=your_password
```

## Navigation

`sw.navigate(folder, item)` uses string keys from `FOLDER_MAP` and `ITEM_MAP`:

**Folders**: `setup`, `switching`, `spanning_tree`, `vlan`, `neighbor_discovery`, `routing`, `qos`, `security`, `diagnostics`, `maintenance`

**Items**: See `ITEM_MAP` in `tasks/__init__.py` (e.g. `port_config`, `vlan_config`, `trunk_config`, `routing_config`, `dual_image`, `backup_update`)

### Important details

- Clicking a folder collapses it. `navigate()` checks item visibility before clicking.
- DataTables pagination is unreliable on firmware 3.4.0 — use raw row iteration.
- Table IDs: `#datagrid-configuration` (VLAN), `#datagrid-trunks` (Trunk), `#datagrid-interface-port` (Port), `#datagrid-routing-vlan` (Routing)
- `sw.apply_pending()` clicks `#btnApply` if pending changes exist (returns True if clicked)
- `sw.download_config()` uses JS fetch to download running config as text

## OLH (Online Help)

Every page embeds HPE help content as CDATA in `<script id="olh...">` tags. Help is loaded **globally** on every page — no navigation required.

```python
# List all help topic IDs
topics = sw.list_help_topics()

# Get help for specific topic (case-insensitive match)
help_html = sw.get_help("SNMPSetting")
help_html = sw.get_help("vlan")

# Get all help
all_help = sw.get_help()
```

**Always check OLH first** when debugging or implementing a new feature.

## API Reference

### `tasks` (base)

| Function | Args | Returns |
|----------|------|---------|
| `connect(ip, cred_file=None)` | switch IP, optional cred file path | `ArubaSwitch` instance |
| `disconnect(sw)` | `ArubaSwitch` instance | None |
| `ArubaSwitch.navigate(folder, item)` | folder key, item key | None |
| `ArubaSwitch.apply_pending()` | — | bool |
| `ArubaSwitch.download_config()` | — | str (config text) |
| `ArubaSwitch.get_firmware_version()` | — | str |
| `ArubaSwitch.get_help(topic=None)` | optional topic string | dict |
| `ArubaSwitch.list_help_topics()` | — | list[str] |

### `vlan`

| Function | Args | Returns |
|----------|------|---------|
| `list_vlans(sw)` | ArubaSwitch | list[(vid, name)] |
| `rename_vlan(sw, vid, new_name)` | ArubaSwitch, int, str | bool |
| `delete_vlan(sw, vid)` | ArubaSwitch, int | bool (raises if blocked) |
| `add_vlan(sw, vid, name)` | ArubaSwitch, int, str | bool |

### `routing`

| Function | Args | Returns |
|----------|------|---------|
| `list_vlan_interfaces(sw)` | ArubaSwitch | list[dict] |
| `clear_vlan_ip(sw, vid)` | ArubaSwitch, int | bool |
| `set_vlan_ip(sw, vid, ip, mask)` | ArubaSwitch, int, str, str | bool |

### `port`

| Function | Args | Returns |
|----------|------|---------|
| `list_ports(sw)` | ArubaSwitch | list[dict] |
| `edit_port_pvid(sw, port, pvid)` | ArubaSwitch, int, int | bool |
| `set_port_description(sw, port, desc)` | ArubaSwitch, int, str | bool |

### `trunk`

| Function | Args | Returns |
|----------|------|---------|
| `list_trunks(sw)` | ArubaSwitch | list[dict] |
| `disable_trunk(sw, trunk_num)` | ArubaSwitch, int | bool |
| `clear_trunk_members(sw, trunk_num)` | ArubaSwitch, int | bool |

### `backup`

| Function | Args | Returns |
|----------|------|---------|
| `backup_config(sw, save_path=None)` | ArubaSwitch, optional path | str (saved path) |
| `get_firmware_info(sw)` | ArubaSwitch | dict |

### `routing` (extended)

| Function | Args | Returns |
|----------|------|---------|
| `add_static_route(sw, destination, mask, gateway, vid)` | ArubaSwitch, str, str, str, int | bool |
| `remove_static_route(sw, idx)` | ArubaSwitch, int | bool |

### `dhcp_relay`

| Function | Args | Returns |
|----------|------|---------|
| `add_dhcp_server(sw, ip)` | ArubaSwitch, str | bool |
| `remove_dhcp_server(sw, ip)` | ArubaSwitch, str | bool |
| `add_dhcp_interface(sw, vid)` | ArubaSwitch, int | bool |
| `remove_dhcp_interface(sw, vid)` | ArubaSwitch, int | bool |

### `logging`

| Function | Args | Returns |
|----------|------|---------|
| `enable_logging(sw)` | ArubaSwitch | bool |
| `set_log_severity(sw, severity)` | ArubaSwitch, str | bool |
| `add_remote_log_server(sw, ip, port)` | ArubaSwitch, str, int | bool |
| `remove_remote_log_server(sw, idx)` | ArubaSwitch, int | bool |

### `loop_protection`

| Function | Args | Returns |
|----------|------|---------|
| `enable_loop_protection(sw)` | ArubaSwitch | bool |
| `set_loop_protection_time(sw, seconds)` | ArubaSwitch, int | bool |
| `set_port_loop_protection(sw, port, enable)` | ArubaSwitch, int, bool | bool |

### `eee_config`

| Function | Args | Returns |
|----------|------|---------|
| `enable_ee(sw)` | ArubaSwitch | bool |
| `enable_low_power(sw)` | ArubaSwitch | bool |

### `maintenance`

| Function | Args | Returns |
|----------|------|---------|
| `reboot_switch(sw)` | ArubaSwitch | None |

### `voice_vlan`

| Function | Args | Returns |
|----------|------|---------|
| `add_telephony_oui(sw, oui)` | ArubaSwitch, str | bool |
| `remove_telephony_oui(sw, oui)` | ArubaSwitch, str | bool |
| `restore_telephony_oui(sw)` | ArubaSwitch | bool |

### `stp_global`

| Function | Args | Returns |
|----------|------|---------|
| `enable_stp(sw)` | ArubaSwitch | bool |
| `set_stp_priority(sw, priority)` | ArubaSwitch, int | bool |
| `set_stp_timers(sw, fwd_delay, hello_time, max_age)` | ArubaSwitch, int, int, int | bool |
| `enable_bpdu_filter(sw)` | ArubaSwitch | bool |

### `mstp_config`

| Function | Args | Returns |
|----------|------|---------|
| `add_mstp_instance(sw, revision, name)` | ArubaSwitch, int, str | bool |
| `edit_mstp_instance(sw, idx, revision, name)` | ArubaSwitch, int, int, str | bool |
| `remove_mstp_instance(sw, idx)` | ArubaSwitch, int | bool |
| `set_mstp_port_params(sw, port, instance, priority, weight)` | ArubaSwitch, int, int, int, int | bool |

### `lldp`

| Function | Args | Returns |
|----------|------|---------|
| `set_lldp_timers(sw, tx_interval, tx_count, hold_time)` | ArubaSwitch, int, int, int | bool |
| `configure_lldp_interface(sw, port, tx, rx)` | ArubaSwitch, int, bool, bool | bool |

### `igmp_snooping`

| Function | Args | Returns |
|----------|------|---------|
| `configure_igmp_snooping(sw, vid, enable, fast_leave)` | ArubaSwitch, int, bool, bool | bool |
| `set_igmp_querier(sw, vid, enable, ip)` | ArubaSwitch, int, bool, str | bool |
| `add_static_member(sw, vid, port, group)` | ArubaSwitch, int, int, str | bool |

### `protected_ports`

| Function | Args | Returns |
|----------|------|---------|
| `enable_protected_port(sw, port)` | ArubaSwitch, int | bool |

### `dos_protection`

| Function | Args | Returns |
|----------|------|---------|
| `enable_dos_protection(sw)` | ArubaSwitch | bool |
| `set_dos_threshold(sw, rate)` | ArubaSwitch, int | bool |

### `arp_attack_protection`

| Function | Args | Returns |
|----------|------|---------|
| `enable_arp_protection(sw)` | ArubaSwitch | bool |
| `set_arp_interface_protection(sw, port, enable)` | ArubaSwitch, int, bool | bool |
| `add_arp_access_rule(sw, vid, mac, ip)` | ArubaSwitch, int, str, str | bool |
| `remove_arp_access_rule(sw, idx)` | ArubaSwitch, int | bool |

### `port_security`

| Function | Args | Returns |
|----------|------|---------|
| `enable_port_security(sw)` | ArubaSwitch | bool |
| `add_static_mac(sw, port, mac)` | ArubaSwitch, int, str | bool |
| `remove_static_mac(sw, idx)` | ArubaSwitch, int | bool |

### `radius`

| Function | Args | Returns |
|----------|------|---------|
| `add_radius_server(sw, ip, port, secret)` | ArubaSwitch, str, int, str | bool |
| `edit_radius_server(sw, idx, ip, port, secret)` | ArubaSwitch, int, str, int, str | bool |
| `remove_radius_server(sw, idx)` | ArubaSwitch, int | bool |

### `schedule_config`

| Function | Args | Returns |
|----------|------|---------|
| `add_schedule(sw, name, type, value)` | ArubaSwitch, str, str, str | bool |
| `remove_schedule(sw, idx)` | ArubaSwitch, int | bool |

### `dhcp_snooping`

| Function | Args | Returns |
|----------|------|---------|
| `enable_dhcp_snooping(sw)` | ArubaSwitch | bool |
| `set_dhcp_trusted_port(sw, port, trusted)` | ArubaSwitch, int, bool | bool |
| `add_dhcp_binding(sw, mac, ip, vid, port)` | ArubaSwitch, str, str, int, int | bool |
| `clear_dhcp_bindings(sw)` | ArubaSwitch | bool |

### `port_mirroring`

| Function | Args | Returns |
|----------|------|---------|
| `add_mirror_session(sw, name, source, direction, dest)` | ArubaSwitch, str, str, str, int | bool |
| `edit_mirror_session(sw, idx, name, source, direction, dest)` | ArubaSwitch, int, str, str, str, int | bool |
| `remove_mirror_session(sw, idx)` | ArubaSwitch, int | bool |

### `snmp`

| Function | Args | Returns |
|----------|------|---------|
| `enable_snmp(sw)` | ArubaSwitch | bool |
| `add_snmp_community(sw, name, access, ip)` | ArubaSwitch, str, str, str | bool |
| `remove_snmp_community(sw, idx)` | ArubaSwitch, int | bool |
| `add_snmp_trap_receiver(sw, name, ip, community)` | ArubaSwitch, str, str, str | bool |
| `remove_snmp_trap_receiver(sw, idx)` | ArubaSwitch, int | bool |

### `acl`

| Function | Args | Returns |
|----------|------|---------|
| `add_acl(sw, name)` | ArubaSwitch, str | bool |
| `add_acl_rule_ipv4(sw, idx, rule)` | ArubaSwitch, int, dict | bool |
| `remove_acl_rule_ipv4(sw, idx, rule_idx)` | ArubaSwitch, int, int | bool |
| `remove_acl(sw, idx)` | ArubaSwitch, int | bool |
| `bind_acl_to_interface(sw, acl_idx, port, direction)` | ArubaSwitch, int, int, str | bool |
| `bind_acl_to_vlan(sw, acl_idx, vid, direction)` | ArubaSwitch, int, int, str | bool |

### `cos`

| Function | Args | Returns |
|----------|------|---------|
| `set_cos_priority(sw, mapping)` | ArubaSwitch, dict | bool |
| `set_queue_scheduling(sw, queue, type, weight)` | ArubaSwitch, int, str, int | bool |
| `set_traffic_type(sw, mapping)` | ArubaSwitch, dict | bool |
| `set_interface_shaping_rate(sw, port, rate)` | ArubaSwitch, int, int | bool |

### `port_access_control`

| Function | Args | Returns |
|----------|------|---------|
| `add_mac_auth_rule(sw, name, action)` | ArubaSwitch, str, str | bool |
| `remove_mac_auth_rule(sw, idx)` | ArubaSwitch, int | bool |
| `add_mac_auth_group(sw, name, rule_idx)` | ArubaSwitch, str, int | bool |
| `remove_mac_auth_group(sw, idx)` | ArubaSwitch, int | bool |
| `set_vlan_authentication(sw, vid, vlan)` | ArubaSwitch, int, int | bool |

### `https_cert`

| Function | Args | Returns |
|----------|------|---------|
| `generate_certificate(sw, cn, key_size, validity)` | ArubaSwitch, str, int, int | bool |
| `import_certificate(sw, cert_path, key_path)` | ArubaSwitch, str, str | bool |
| `delete_certificate(sw, idx)` | ArubaSwitch, int | bool |

## Firmware Compatibility

Tested on InstantOn_1930_3.4.0. Table IDs and selectors may differ on other versions.

## License

BSD 2-Clause. See [LICENSE](LICENSE).

## AI Attribution

This work was generated by a human-guided AI assistant. The model is Qwen3.6-27B-Q4 (pooled/qwen3.6-27b-q4), hosted locally on three NVIDIA GPUs (1x GeForce RTX 3060, 2x GeForce GTX 1080 Ti). No cloud APIs were used.
