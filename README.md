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
- **`routing`**: VLAN IP interface management — list, clear, set static IP. Uses `#datagrid-routing-vlan`.
- **`port`**: Port configuration — list, set PVID, set description. Uses `#datagrid-interface-port`.
- **`trunk`**: Trunk management — list, disable, clear members. Uses `#datagrid-trunks`. Note: web UI does NOT support trunk removal.
- **`backup`**: Config download and firmware info extraction.

## Usage

```python
from tasks import connect, disconnect
from tasks import vlan, routing, port, trunk, backup

sw = connect("192.168.27.2")  # switch IP
try:
    # List VLANs
    vlans = vlan.list_vlans(sw)

    # Rename VLAN
    vlan.rename_vlan(sw, 3, "home")

    # Set port PVID
    port.edit_port_pvid(sw, 1, 3)

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

## Firmware Compatibility

Tested on InstantOn_1930_3.4.0. Table IDs and selectors may differ on other versions.

## License

BSD 2-Clause. See [LICENSE](LICENSE).

## AI Attribution

This work was generated by a human-guided AI assistant. The model is Qwen3.6-27B-Q4 (pooled/qwen3.6-27b-q4), hosted locally on three NVIDIA GPUs (1x GeForce RTX 3060, 2x GeForce GTX 1080 Ti). No cloud APIs were used.
