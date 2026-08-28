"""Write operations for maintenance (reboot)."""
from tasks import ArubaSwitch


def reboot_switch(sw: ArubaSwitch, save_config: bool = True) -> bool:
    """Reboot the switch.

    Args:
        save_config: If True, save running config before reboot.

    Returns:
        True if reboot initiated.

    Warning: This disconnects the browser session. Do not call disconnect()
    after this function.
    """
    sw.navigate('maintenance', 'reset')
    sw.page.wait_for_timeout(2000)

    btn = sw.page.query_selector("#btnReboot")
    if not btn:
        raise RuntimeError("Reboot button not found")

    btn.click()
    sw.page.wait_for_timeout(1500)

    confirm = sw.page.query_selector(".modal.show")
    if not confirm:
        raise RuntimeError("Reboot confirmation modal not found")

    if save_config:
        apply_btn = confirm.query_selector("#modalConfirmButtonSaveReboot")
        if apply_btn:
            apply_btn.click()
    else:
        apply_btn = confirm.query_selector("#modalConfirmButtonReboot")
        if apply_btn:
            apply_btn.click()

    sw.page.wait_for_timeout(2000)
    return True
