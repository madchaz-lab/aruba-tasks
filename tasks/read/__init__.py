"""Read-only API operations for Aruba Instant On 1930 switches."""
from tasks.read.vlan import list_vlans
from tasks.read.routing import list_vlan_interfaces
from tasks.read.port import list_ports
from tasks.read.trunk import list_trunks
from tasks.read.backup import backup_config, get_firmware_info

__all__ = [
    "list_vlans",
    "list_vlan_interfaces",
    "list_ports",
    "list_trunks",
    "backup_config",
    "get_firmware_info",
]
