"""Read operations for Maintenance configuration.

OLH topics: olhMaintenance, olhConfigurationFile, olhRebootDevice,
            olhReset, olhResetDefaults, olhConfigWizard
"""
from tasks import ArubaSwitch


def get_config_file_info(sw: ArubaSwitch):
    """Return dict with config file information.

    OLH: olhMaintenance
    """
    sw.navigate('maintenance', 'backup_update')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Config')) {
                    if (i + 1 < lines.length) {
                        result.config = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_reboot_status(sw: ArubaSwitch):
    """Return dict with reboot status and configuration.

    OLH: olhRebootDevice
    """
    sw.navigate('maintenance', 'reset')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.can_reboot = body.includes('REBOOT');
            return result;
        }
    """)


def get_reset_status(sw: ArubaSwitch):
    """Return dict with reset status and configuration.

    OLH: olhReset
    """
    sw.navigate('maintenance', 'reset')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.has_unsaved_changes = body.includes('unsaved changes');
            return result;
        }
    """)


def get_reset_defaults_status(sw: ArubaSwitch):
    """Return dict with reset to defaults status.

    OLH: olhResetDefaults
    """
    sw.navigate('maintenance', 'reset')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.can_reset = body.includes('Reset to Factory Defaults');
            return result;
        }
    """)


def get_config_wizard_status(sw: ArubaSwitch):
    """Return dict with config wizard status.

    OLH: olhConfigWizard
    """
    sw.navigate('setup', 'get_connected')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Management Address Type')) {
                    if (i + 1 < lines.length) {
                        result.address_type = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
