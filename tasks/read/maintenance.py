"""Read operations for Maintenance.

OLH topics: olhMaintenance, olhConfigFile
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
