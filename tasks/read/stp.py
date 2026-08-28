"""Read operations for STP (Spanning Tree Protocol) configuration.

OLH topics: olhSTP, olhSTPGlobal, olhSTPStatistics
"""
from tasks import ArubaSwitch


def get_stp_global_status(sw: ArubaSwitch):
    """Return dict with STP global status.

    OLH: olhSTP
    """
    sw.navigate('spanning_tree', 'stp_global')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_stp_statistics(sw: ArubaSwitch):
    """Return dict with STP statistics.

    OLH: olhSTPStatistics
    """
    sw.navigate('spanning_tree', 'stp_global')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Tx BPDUs')) {
                    if (i + 1 < lines.length) {
                        result.tx_bpdus = lines[i + 1];
                    }
                }
                if (line.includes('Rx BPDUs')) {
                    if (i + 1 < lines.length) {
                        result.rx_bpdus = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
