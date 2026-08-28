"""Write (config-changing) API operations for Aruba Instant On 1930 switches."""
from tasks.write.vlan import add_vlan, rename_vlan, delete_vlan
from tasks.write.routing import clear_vlan_ip, set_vlan_ip
from tasks.write.port import edit_port_pvid, set_port_description
from tasks.write.trunk import disable_trunk, clear_trunk_members

__all__ = [
    "add_vlan",
    "rename_vlan",
    "delete_vlan",
    "clear_vlan_ip",
    "set_vlan_ip",
    "edit_port_pvid",
    "set_port_description",
    "disable_trunk",
    "clear_trunk_members",
]
