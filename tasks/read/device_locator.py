"""Read operations for Device Locator.

OLH topics: olhDeviceLocator
"""
from tasks import ArubaSwitch


def get_device_locator_status(sw: ArubaSwitch):
    """Return dict with device locator status.

    OLH: olhDeviceLocator
    """
    sw.navigate('diagnostics', 'cable_test')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('Enabled');
            return result;
        }
    """)
