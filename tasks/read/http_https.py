"""Read operations for HTTP/HTTPS configuration.

OLH topics: olhHTTP, olhHTTPS, olhCertificate
"""
from tasks import ArubaSwitch


def get_http_settings(sw: ArubaSwitch):
    """Return dict with HTTP settings.

    OLH: olhHTTP
    """
    sw.navigate('setup', 'get_connected')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('HTTP');
            return result;
        }
    """)


def get_https_settings(sw: ArubaSwitch):
    """Return dict with HTTPS settings.

    OLH: olhHTTPS
    """
    sw.navigate('security', 'https_cert')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            result.enabled = body.includes('HTTPS');
            return result;
        }
    """)


def get_certificate_info(sw: ArubaSwitch):
    """Return dict with certificate information.

    OLH: olhCertificate
    """
    sw.navigate('security', 'https_cert')
    sw.page.wait_for_timeout(4000)
    return sw.page.evaluate("""
        () => {
            const body = document.body.innerText;
            const result = {};
            const lines = body.split('\\n').map(l => l.trim()).filter(l => l);
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.includes('Certificate')) {
                    if (i + 1 < lines.length) {
                        result.certificate = lines[i + 1];
                    }
                }
            }
            return result;
        }
    """)
