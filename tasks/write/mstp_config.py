"""Write operations for MSTP configuration."""
from tasks import ArubaSwitch


def add_mstp_instance(sw: ArubaSwitch, mstp_id: int, priority: int = 32768, vlan_ids: list = None) -> bool:
    """Add an MSTP instance. Returns True if applied.

    Args:
        mstp_id: MSTP instance ID
        priority: Bridge priority for this instance
        vlan_ids: List of VLAN IDs to map to this instance
    """
    sw.navigate('spanning_tree', 'mstp_config')
    sw.page.wait_for_timeout(2000)

    sw.page.click("#mstp-add")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Add MSTP modal not found")

    sw.page.evaluate(f"jQuery('#mstpIDInput').val('{mstp_id}').trigger('change');")

    sw.page.evaluate(f"""
        () => {{
            jQuery('#slctPriorityAdd').val({priority}).trigger('change');
        }}
    """)

    if vlan_ids:
        for vid in vlan_ids:
            sw.page.evaluate(f"""
                () => {{
                    jQuery('#multiselectAdd option').filter(function() {{
                        return this.text === '{vid}';
                    }}).prop('selected', true).parent().trigger('change');
                    document.getElementById('multiselectAdd_rightSelected').click();
                }}
            """)
            sw.page.wait_for_timeout(300)

    sw.page.evaluate("document.getElementById('modalAddButtonApply').click()")
    sw.page.wait_for_timeout(2000)
    # Wait for modal to close
    sw.page.wait_for_selector(".modal.show", state="hidden", timeout=5000)
    sw.apply_pending()
    return True


def edit_mstp_instance(sw: ArubaSwitch, mstp_id: int, priority: int = None, vlan_ids: list = None) -> bool:
    """Edit an existing MSTP instance. Returns True if applied."""
    sw.navigate('spanning_tree', 'mstp_config')
    sw.page.click("#mstp-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-mstp').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.instanceID === '{mstp_id}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"MSTP instance {mstp_id} not found")

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-mstp').DataTable().row({row_idx}).select();
            document.getElementById('mstp-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit MSTP modal not found")

    if priority is not None:
        sw.page.evaluate(f"""
            () => {{
                jQuery('#slctPriorityEdit').val({priority}).trigger('change');
            }}
        """)

    if vlan_ids:
        for vid in vlan_ids:
            sw.page.evaluate(f"""
                () => {{
                    jQuery('#multiselectEdit option').filter(function() {{
                        return this.text === '{vid}';
                    }}).prop('selected', true).parent().trigger('change');
                    document.getElementById('multiselectEdit_rightSelected').click();
                }}
            """)
            sw.page.wait_for_timeout(300)

    modal.query_selector("#modalEditButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True


def remove_mstp_instance(sw: ArubaSwitch, mstp_id: int) -> bool:
    """Remove an MSTP instance. Returns True if removed, False if not found."""
    sw.navigate('spanning_tree', 'mstp_config')
    sw.page.click("#mstp-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-mstp').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.instanceID === '{mstp_id}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        return False

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-mstp').DataTable().row({row_idx}).select();
            document.getElementById('mstp-remove').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)
    sw.apply_pending()
    return True


def set_mstp_port_params(sw: ArubaSwitch, port: int, priority: int = None, path_cost: int = None) -> bool:
    """Set MSTP port priority and path cost. Returns True if applied.

    Args:
        port: Port number
        priority: Port priority (0-240, multiple of 16)
        path_cost: Port path cost
    """
    sw.navigate('spanning_tree', 'mstp_config')
    sw.page.click("#mstp-port-refresh")
    sw.page.wait_for_timeout(1000)

    row_idx = sw.page.evaluate(f"""
        () => {{
            const dt = jQuery('#datagrid-mstp-port').DataTable();
            for (let i = 0; i < dt.rows().count(); i++) {{
                const data = dt.row(i).data();
                if (data && data.interfaceName === '{port}') return i;
            }}
            return -1;
        }}
    """)
    if row_idx < 0:
        raise ValueError(f"Port {port} not found in MSTP port table")

    sw.page.evaluate(f"""
        () => {{
            jQuery('#datagrid-mstp-port').DataTable().row({row_idx}).select();
            document.getElementById('mstp-port-edit').click();
        }}
    """)
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Edit MSTP port modal not found")

    if priority is not None:
        sel = modal.query_selector("#slctMstpPortPriorityEdit")
        if sel:
            sel.select_option(label=str(priority))

    if path_cost is not None:
        inp = modal.query_selector("#portPathCostEdit")
        if inp:
            inp.fill(str(path_cost))

    modal.query_selector("#modalEditMSTPPortButtonApply").click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True
