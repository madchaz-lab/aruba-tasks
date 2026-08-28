"""Read operations for System configuration.

OLH topics: olhSystem, olhSystemInformation, olhSystemTime, olhSystemResources,
            olhUserManagement, olhPasswordRules, olhUserSessions, olhManagementVLAN,
            olhDaylightSaving, olhDashboard, olhDashboardDeviceView, olhDeviceInformation
"""
from tasks import ArubaSwitch


def get_dashboard_info(sw: ArubaSwitch):
    """Return dict with dashboard information.

    OLH: olhDashboard
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
                if (line.includes('Software Version')) {
                    if (i + 1 < lines.length) {
                        result.software_version = lines[i + 1];
                    }
                }
                if (line.includes('CPU Utilization')) {
                    if (i + 1 < lines.length) {
                        result.cpu_utilization = lines[i + 1];
                    }
                }
                if (line.includes('Memory Usage')) {
                    if (i + 1 < lines.length) {
                        result.memory_usage = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_dashboard_device_view(sw: ArubaSwitch):
    """Return dict with dashboard device view.

    OLH: olhDashboardDeviceView
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
                if (line.includes('System Resource')) {
                    if (i + 1 < lines.length) {
                        result.system_resource = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_device_information(sw: ArubaSwitch):
    """Return dict with device information.

    OLH: olhDeviceInformation
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
                if (line.includes('Software Version')) {
                    if (i + 1 < lines.length) {
                        result.software_version = lines[i + 1];
                    }
                }
                if (line.includes('OS Version')) {
                    if (i + 1 < lines.length) {
                        result.os_version = lines[i + 1];
                    }
                }
                if (line.includes('Serial Number')) {
                    if (i + 1 < lines.length) {
                        result.serial_number = lines[i + 1];
                    }
                }
                if (line.includes('MAC Address')) {
                    if (i + 1 < lines.length) {
                        result.mac_address = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_system_info(sw: ArubaSwitch):
    """Return dict with system information.

    OLH: olhSystem
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
                if (line.includes('Software Version')) {
                    if (i + 1 < lines.length) {
                        result.software_version = lines[i + 1];
                    }
                }
                if (line.includes('Serial Number')) {
                    if (i + 1 < lines.length) {
                        result.serial_number = lines[i + 1];
                    }
                }
                if (line.includes('MAC Address')) {
                    if (i + 1 < lines.length) {
                        result.mac_address = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_system_time(sw: ArubaSwitch):
    """Return dict with system time settings.

    OLH: olhSystemTime
    """
    sw.navigate('setup', 'system_time')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Current Time')) {
                    if (i + 1 < lines.length) {
                        result.current_time = lines[i + 1];
                    }
                }
                if (line.includes('NTP Server')) {
                    if (i + 1 < lines.length) {
                        result.ntp_server = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_system_resources(sw: ArubaSwitch):
    """Return dict with system resource usage.

    OLH: olhSystemResources
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
                if (line.includes('CPU Usage')) {
                    if (i + 1 < lines.length) {
                        result.cpu_usage = lines[i + 1];
                    }
                }
                if (line.includes('Memory Usage')) {
                    if (i + 1 < lines.length) {
                        result.memory_usage = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def list_user_accounts(sw: ArubaSwitch):
    """Return list of dicts with user account information.

    OLH: olhUserManagement
    """
    sw.navigate('setup', 'user_management')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-user-management').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def get_password_rules(sw: ArubaSwitch):
    """Return dict with password rules.

    OLH: olhPasswordRules
    """
    sw.navigate('setup', 'user_management')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Minimum Length')) {
                    if (i + 1 < lines.length) {
                        result.min_length = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def list_user_sessions(sw: ArubaSwitch):
    """Return list of dicts with active user sessions.

    OLH: olhUserSessions
    """
    sw.navigate('setup', 'user_management')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('User') || headers.includes('Session')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 2) {
                            result.push({
                                user: cells[0].innerText.trim(),
                                ip_address: cells[1].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def get_management_vlan(sw: ArubaSwitch):
    """Return dict with management VLAN settings.

    OLH: olhManagementVLAN
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
                if (line.includes('Management VLAN')) {
                    if (i + 1 < lines.length) {
                        result.management_vlan = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)


def get_daylight_saving(sw: ArubaSwitch):
    """Return dict with daylight saving time settings.

    OLH: olhDaylightSaving
    """
    sw.navigate('setup', 'system_time')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)


def get_logged_in_sessions(sw: ArubaSwitch):
    """Return list of dicts with logged-in user sessions.

    OLH: olhLoggedIn
    """
    sw.navigate('setup', 'user_management')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Username') && headers.includes('Session Time')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 4) {
                            result.push({
                                username: cells[0].innerText.trim(),
                                connected_from: cells[1].innerText.trim(),
                                session_time: cells[2].innerText.trim(),
                                session_type: cells[3].innerText.trim()
                            });
                        }
                    });
                }
            });
            return result;
        }
    """)


def list_password_keywords(sw: ArubaSwitch):
    """Return list of dicts with password keyword exclusion list.

    OLH: olhKeywords
    """
    sw.navigate('setup', 'user_management')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const result = [];
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
                if (headers.includes('Keyword')) {
                    const rows = Array.from(table.querySelectorAll('tbody tr'));
                    rows.forEach(row => {
                        const cells = Array.from(row.querySelectorAll('td'));
                        if (cells.length >= 1 && !cells[0].innerText.trim().includes('Table Is Empty')) {
                            result.push({ keyword: cells[0].innerText.trim() });
                        }
                    });
                }
            });
            return result;
        }
    """)
