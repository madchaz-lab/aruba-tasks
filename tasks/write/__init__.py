"""Write (config-changing) API operations for Aruba Instant On 1930 switches."""
from tasks.write.vlan import add_vlan, rename_vlan, delete_vlan
from tasks.write.routing import clear_vlan_ip, set_vlan_ip, add_static_route, remove_static_route
from tasks.write.port import edit_port_pvid, set_port_description
from tasks.write.trunk import disable_trunk, clear_trunk_members
from tasks.write.dhcp_relay import (
    add_dhcp_server, remove_dhcp_server,
    add_dhcp_interface, remove_dhcp_interface,
)
from tasks.write.logging import (
    enable_logging, set_log_severity,
    add_remote_log_server, remove_remote_log_server,
)
from tasks.write.loop_protection import (
    enable_loop_protection, set_loop_protection_time, set_port_loop_protection,
)
from tasks.write.eee_config import enable_ee, enable_low_power
from tasks.write.maintenance import reboot_switch
from tasks.write.voice_vlan import (
    add_telephony_oui, remove_telephony_oui, restore_telephony_oui,
)
from tasks.write.stp_global import (
    enable_stp, set_stp_priority, set_stp_timers, enable_bpdu_filter,
)
from tasks.write.mstp_config import (
    add_mstp_instance, edit_mstp_instance,
    remove_mstp_instance, set_mstp_port_params,
)
from tasks.write.lldp import set_lldp_timers, configure_lldp_interface
from tasks.write.igmp_snooping import (
    configure_igmp_snooping, set_igmp_querier, add_static_member,
)
from tasks.write.protected_ports import enable_protected_port
from tasks.write.dos_protection import enable_dos_protection, set_dos_threshold
from tasks.write.arp_attack_protection import (
    enable_arp_protection, set_arp_interface_protection,
    add_arp_access_rule, remove_arp_access_rule,
)
from tasks.write.port_security import enable_port_security, add_static_mac, remove_static_mac
from tasks.write.radius import add_radius_server, edit_radius_server, remove_radius_server
from tasks.write.schedule_config import add_schedule, remove_schedule
from tasks.write.dhcp_snooping import (
    enable_dhcp_snooping, set_dhcp_trusted_port,
    add_dhcp_binding, clear_dhcp_bindings,
)
from tasks.write.port_mirroring import (
    add_mirror_session, edit_mirror_session, remove_mirror_session,
)
from tasks.write.snmp import (
    enable_snmp, add_snmp_community, remove_snmp_community,
    add_snmp_trap_receiver, remove_snmp_trap_receiver,
)
from tasks.write.acl import (
    add_acl, add_acl_rule_ipv4, remove_acl_rule_ipv4,
    remove_acl, bind_acl_to_interface, bind_acl_to_vlan,
)
from tasks.write.cos import (
    set_cos_priority, set_queue_scheduling,
    set_traffic_type, set_interface_shaping_rate,
)
from tasks.write.port_access_control import (
    add_mac_auth_rule, remove_mac_auth_rule,
    add_mac_auth_group, remove_mac_auth_group,
    set_vlan_authentication,
)

__all__ = [
    # VLAN
    "add_vlan", "rename_vlan", "delete_vlan",
    # Routing
    "clear_vlan_ip", "set_vlan_ip", "add_static_route", "remove_static_route",
    # Port
    "edit_port_pvid", "set_port_description",
    # Trunk
    "disable_trunk", "clear_trunk_members",
    # DHCP Relay
    "add_dhcp_server", "remove_dhcp_server",
    "add_dhcp_interface", "remove_dhcp_interface",
    # Logging
    "enable_logging", "set_log_severity",
    "add_remote_log_server", "remove_remote_log_server",
    # Loop Protection
    "enable_loop_protection", "set_loop_protection_time", "set_port_loop_protection",
    # EEE
    "enable_ee", "enable_low_power",
    # Maintenance
    "reboot_switch",
    # Voice VLAN
    "add_telephony_oui", "remove_telephony_oui", "restore_telephony_oui",
    # STP
    "enable_stp", "set_stp_priority", "set_stp_timers", "enable_bpdu_filter",
    # MSTP
    "add_mstp_instance", "edit_mstp_instance",
    "remove_mstp_instance", "set_mstp_port_params",
    # LLDP
    "set_lldp_timers", "configure_lldp_interface",
    # IGMP Snooping
    "configure_igmp_snooping", "set_igmp_querier", "add_static_member",
    # Protected Ports
    "enable_protected_port",
    # DoS Protection
    "enable_dos_protection", "set_dos_threshold",
    # ARP Attack Protection
    "enable_arp_protection", "set_arp_interface_protection",
    "add_arp_access_rule", "remove_arp_access_rule",
    # Port Security
    "enable_port_security", "add_static_mac", "remove_static_mac",
    # RADIUS
    "add_radius_server", "edit_radius_server", "remove_radius_server",
    # Schedule
    "add_schedule", "remove_schedule",
    # DHCP Snooping
    "enable_dhcp_snooping", "set_dhcp_trusted_port",
    "add_dhcp_binding", "clear_dhcp_bindings",
    # Port Mirroring
    "add_mirror_session", "edit_mirror_session", "remove_mirror_session",
    # SNMP
    "enable_snmp", "add_snmp_community", "remove_snmp_community",
    "add_snmp_trap_receiver", "remove_snmp_trap_receiver",
    # ACL
    "add_acl", "add_acl_rule_ipv4", "remove_acl_rule_ipv4",
    "remove_acl", "bind_acl_to_interface", "bind_acl_to_vlan",
    # CoS
    "set_cos_priority", "set_queue_scheduling",
    "set_traffic_type", "set_interface_shaping_rate",
    # Port Access Control
    "add_mac_auth_rule", "remove_mac_auth_rule",
    "add_mac_auth_group", "remove_mac_auth_group",
    "set_vlan_authentication",
]
