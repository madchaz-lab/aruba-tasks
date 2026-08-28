"""Read operations for Logging.

OLH topics: olhLogging, olhLoggingGlobal, olhBufferedLogs, olhLogMessages, olhRemoteLogging
"""
from tasks import ArubaSwitch


def get_log_global_config(sw: ArubaSwitch):
    """Return dict with logging global configuration.

    OLH: olhLogging
    """
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def list_buffered_logs(sw: ArubaSwitch):
    """Return list of dicts with buffered log entries.

    OLH: olhBufferedLogs
    """
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = [];
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].includes('[') && lines[i].includes(']')) {
                    result.push({ message: lines[i] });
                }
            }
            return result;
        }
    """)


def list_log_messages(sw: ArubaSwitch):
    """Return list of dicts with log messages.

    OLH: olhLogMessages
    """
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = [];
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].length > 10) {
                    result.push({ message: lines[i] });
                }
            }
            return result;
        }
    """)


def get_log_file(sw: ArubaSwitch):
    """Return dict with log file information.

    OLH: olhLoggingLogFile
    """
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Log File')) {
                    if (i + 1 < lines.length) {
                        result.log_file = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_remote_log_config(sw: ArubaSwitch):
    """Return dict with remote logging configuration.

    OLH: olhRemoteLogging
    """
    sw.navigate('diagnostics', 'logging')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Server')) {
                    if (i + 1 < lines.length) {
                        result.server = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
