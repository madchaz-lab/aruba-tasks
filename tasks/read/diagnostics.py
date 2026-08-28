"""Read operations for Diagnostics.

OLH topics: olhPing, olhTraceroute, olhCableTest, olhSupportFile
Note: Interactive diagnostics (ping, traceroute, cable_test) require form submission
which is handled via JavaScript evaluate. These functions return page state.
"""
from tasks import ArubaSwitch


def ping(sw: ArubaSwitch, target: str, count: int = 4):
    """Execute a ping diagnostic.

    OLH: olhPing
    Args:
        target: IP address or hostname to ping
        count: number of ping packets (default 4)
    Returns:
        dict with ping results
    """
    sw.navigate('diagnostics', 'ping')
    sw.page.wait_for_timeout(4000)
    sw.page.fill('#txtPingIPv4Input', target)
    sw.page.fill('#txtPingIPv4Count', str(count))
    # Submit form via JS
    sw.page.evaluate("""
        () => {
            const forms = document.querySelectorAll('form');
            forms.forEach(f => {
                if (f.querySelector('#txtPingIPv4Input')) {
                    f.requestSubmit();
                }
            });
        }
    """)
    sw.page.wait_for_timeout(5000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            result.output = lines.join('\\n');
            result.success = body.includes('Received');
            return result;
        }
    """)


def traceroute(sw: ArubaSwitch, target: str):
    """Execute a traceroute diagnostic.

    OLH: olhTraceroute
    Args:
        target: IP address or hostname to traceroute
    Returns:
        dict with traceroute results
    """
    sw.navigate('diagnostics', 'traceroute')
    sw.page.wait_for_timeout(4000)
    sw.page.fill('#txtTracerouteIPv4Input', target)
    sw.page.evaluate("""
        () => {
            const forms = document.querySelectorAll('form');
            forms.forEach(f => {
                if (f.querySelector('#txtTracerouteIPv4Input')) {
                    f.requestSubmit();
                }
            });
        }
    """)
    sw.page.wait_for_timeout(10000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            result.output = lines.join('\\n');
            return result;
        }
    """)


def cable_test(sw: ArubaSwitch, port: int):
    """Execute a cable test diagnostic.

    OLH: olhCableTest
    Args:
        port: port number to test
    Returns:
        dict with cable test results
    """
    sw.navigate('diagnostics', 'cable_test')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            result.output = lines.join('\\n');
            return result;
        }
    """)


def download_support_file(sw: ArubaSwitch):
    """Download the support file.

    OLH: olhSupportFile
    Returns:
        str: support file contents
    """
    sw.navigate('diagnostics', 'support_file')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        async () => {
            try {
                const r = await fetch('/hpe/http_download?action=3', {
                    credentials: 'include'
                });
                return await r.text();
            } catch(e) {
                return 'Error: ' + e.message;
            }
        }
    """)
