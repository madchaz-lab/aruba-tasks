"""Read operations for LLDP-MED configuration.

OLH topics: olhLLDPMED, olhLLDPMEDConfiguration, olhLLDPMEDInformation,
            olhLLDPMEDInterface, olhLLDPMEDRemote
"""
from tasks import ArubaSwitch


def get_lldpmed_global(sw: ArubaSwitch):
    """Return dict with LLDP-MED global settings.

    OLH: olhLLDPMED, olhLLDPMEDConfiguration
    """
    sw.navigate('neighbor_discovery', 'lldp_med')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Fast Start Repeat Counter')) {
                    if (i + 1 < lines.length) {
                        result.fast_start_repeat = lines[i + 1];
                    }
                }
                if (line.includes('Device Class')) {
                    if (i + 1 < lines.length) {
                        result.device_class = lines[i + 1];
                    }
                }
                if (line.includes('Network Connectivity')) {
                    if (i + 1 < lines.length) {
                        result.network_connectivity = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_lldpmed_information(sw: ArubaSwitch):
    """Return dict with LLDP-MED global information.

    OLH: olhLLDPMEDInformation
    """
    sw.navigate('neighbor_discovery', 'lldp_med')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Chassis ID')) {
                    if (i + 1 < lines.length) {
                        result.chassis_id = lines[i + 1];
                    }
                }
                if (line.includes('Capabilities Supported')) {
                    if (i + 1 < lines.length) {
                        result.capabilities_supported = lines[i + 1];
                    }
                }
                if (line.includes('Capabilities Enabled')) {
                    if (i + 1 < lines.length) {
                        result.capabilities_enabled = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_lldpmed_per_interface(sw: ArubaSwitch):
    """Return list of dicts with LLDP-MED per interface settings.

    OLH: olhLLDPMEDInterface
    Table: #datagrid-interface-lldpmed
    """
    sw.navigate('neighbor_discovery', 'lldp_med')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-interface-lldpmed').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_lldpmed_remote_devices(sw: ArubaSwitch):
    """Return list of dicts with LLDP-MED remote device information.

    OLH: olhLLDPMEDRemote
    Table: #datagrid-remote-devices-lldp-med
    """
    sw.navigate('neighbor_discovery', 'lldp_med')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-remote-devices-lldp-med').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
