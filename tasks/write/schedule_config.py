"""Write operations for PoE schedule configuration."""
from tasks import ArubaSwitch

SCHEDULE_TABLE = '#datagrid-poe-schedule'


def add_schedule(sw: ArubaSwitch, schedule_name: str, schedule_type: str = "once",
                 start_date: str = None, start_time: str = None,
                 end_date: str = None, end_time: str = None) -> bool:
    """Add a PoE schedule. Returns True if applied.

    Args:
        schedule_name: Name to select from dropdown
        schedule_type: 'once' or 'recurring'
        start_date: Start date (YYYY-MM-DD)
        start_time: Start time (HH:MM)
        end_date: End date (YYYY-MM-DD)
        end_time: End time (HH:MM)
    """
    sw.navigate('setup', 'schedule_config')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#poe-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add modal not found")

    radio_id = "rbType_0" if schedule_type == "once" else "rbType_1"
    sw.page.evaluate(f"document.getElementById('{radio_id}').click()")
    sw.page.wait_for_timeout(500)

    if start_date is not None:
        date_inp = modal.query_selector("[name='dateStartDate']")
        if date_inp:
            date_inp.fill(start_date)

    if start_time is not None:
        time_inp = modal.query_selector("[name='txtStartTimeOfDay']")
        if time_inp:
            time_inp.fill(start_time)

    if end_date is not None:
        date_inp = modal.query_selector("[name='dateEndDate']")
        if date_inp:
            date_inp.fill(end_date)

    if end_time is not None:
        time_inp = modal.query_selector("[name='txtEndTimeOfDay']")
        if time_inp:
            time_inp.fill(end_time)

    modal.query_selector("#modalAddButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_schedule(sw: ArubaSwitch, schedule_name: str) -> bool:
    """Remove a PoE schedule. Returns True if removed, False if not found."""
    sw.navigate('setup', 'schedule_config')
    sw.page.click("#poe-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('{SCHEDULE_TABLE}').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.toString().includes('{schedule_name}')) return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('{SCHEDULE_TABLE}').DataTable().row({row_idx}).select();
            document.getElementById('poe-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True
