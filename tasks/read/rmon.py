"""Read operations for RMON configuration.

OLH topics: olhRMON, olhRMONAlarms, olhRMONCollectors, olhRMONEvents, olhRMONStatistics
"""
from tasks import ArubaSwitch


def list_rmon_alarms(sw: ArubaSwitch):
    """Return list of dicts with RMON alarm configuration.

    OLH: olhRMONAlarms
    """
    sw.navigate('diagnostics', 'rmon')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-rmon-alarm').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_rmon_collectors(sw: ArubaSwitch):
    """Return list of dicts with RMON collector configuration.

    OLH: olhRMONCollectors
    """
    sw.navigate('diagnostics', 'rmon')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-rmon-collector').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_rmon_events(sw: ArubaSwitch):
    """Return list of dicts with RMON event configuration.

    OLH: olhRMONEvents
    """
    sw.navigate('diagnostics', 'rmon')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-rmon-event').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)


def list_rmon_statistics(sw: ArubaSwitch):
    """Return list of dicts with RMON statistics.

    OLH: olhRMONStatistics
    """
    sw.navigate('diagnostics', 'rmon')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const dt = jQuery('#datagrid-rmon-statistics').DataTable();
            const result = [];
            for (let i = 0; i < dt.rows().count(); i++) {
                result.push(dt.row(i).data());
            }
            return result;
        }
    """)
