"""Read operations for config backup and firmware info."""
import os
from tasks import ArubaSwitch


def backup_config(sw: ArubaSwitch, save_path: str = None):
    """Download running config and save to file.

    Args:
        sw: ArubaSwitch instance
        save_path: output file path. If None, uses aruba/<hostname>.cfg
    """
    config = sw.download_config()
    if save_path is None:
        hostname = "switch"
        for line in config.split('\n')[:10]:
            if line.startswith('hostname '):
                hostname = line.split()[1]
                break
        save_path = os.path.join(os.path.dirname(__file__), '..', '..', f"{hostname}.cfg")

    with open(save_path, 'w') as f:
        f.write(config)
    return save_path


def get_firmware_info(sw: ArubaSwitch):
    """Return firmware version and system info dict.

    Returns dict with keys: active_version, backup_version, next_active
    """
    sw.navigate('maintenance', 'dual_image')
    sw.page.wait_for_timeout(2000)

    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const active = body.match(/Active Image Version\\s*([\\d.]+)/);
            if (active) result.active_version = active[1];
            const backup = body.match(/Backup Image Version\\s*([\\d.]+)/);
            if (backup) result.backup_version = backup[1];
            const next = body.match(/Next Active Image\\s*(.+?)(?=REFRESH|$)/s);
            if (next) result.next_active = next[1].trim();
            return result;
        }
    """)
