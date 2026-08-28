"""Write operations for HTTPS certificate configuration."""
from tasks import ArubaSwitch


def generate_certificate(sw: ArubaSwitch, common_name: str = "",
                         org_unit: str = "", org_name: str = "",
                         location: str = "", state: str = "",
                         country: str = "", duration: int = 365,
                         key_type: str = "RSA", key_length: int = 2048) -> bool:
    """Generate a self-signed HTTPS certificate. Returns True if applied.

    Args:
        common_name: Common name (default: switch IP)
        org_unit: Organizational unit
        org_name: Organization name
        location: Location/city
        state: State/province
        country: Country code
        duration: Certificate validity in days
        key_type: 'RSA' (only supported type)
        key_length: Key length (2048 or 4096)
    """
    sw.navigate('security', 'https_cert')
    sw.page.wait_for_timeout(2000)

    sw.page.click("button:has-text('GENERATE CERTIFICATE')")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Generate certificate modal not found")

    sw.page.evaluate(f"""
        () => {{
            const fields = [
                'txtGenerateCertificateName',
                'txtGenerateCertificateOrgUnit',
                'txtGenerateCertificateOrgName',
                'txtGenerateCertificateLocation',
                'txtGenerateCertificateState',
                'txtGenerateCertificateCountry',
                'txtGenerateCertificateDuration',
            ];
            const values = [
                '{common_name}',
                '{org_unit}',
                '{org_name}',
                '{location}',
                '{state}',
                '{country}',
                '{duration}',
            ];
            for (let i = 0; i < fields.length; i++) {{
                const el = document.getElementById(fields[i]);
                if (el) el.value = values[i];
            }}
        }}
    """)
    sw.page.wait_for_timeout(500)

    if key_type == "RSA":
        chk = modal.query_selector("#chckGenerateCertificateRSAKey")
        if chk and not chk.is_checked():
            sw.page.evaluate("document.getElementById('chckGenerateCertificateRSAKey').click()")
            sw.page.wait_for_timeout(500)

    if key_length == 4096:
        sw.page.evaluate("document.getElementById('rdoGenerateCertificateKeyLength_1').click()")
        sw.page.wait_for_timeout(500)
    elif key_length == 2048:
        sw.page.evaluate("document.getElementById('rdoGenerateCertificateKeyLength_0').click()")
        sw.page.wait_for_timeout(500)

    modal.query_selector("#generateCertificateButtonApply").click()
    sw.page.wait_for_timeout(3000)
    sw.apply_pending()
    return True


def import_certificate(sw: ArubaSwitch, cert_pem: str,
                       include_keys: bool = False,
                       public_key: str = "", private_key: str = "") -> bool:
    """Import an HTTPS certificate. Returns True if applied.

    Args:
        cert_pem: PEM-encoded certificate
        include_keys: Include public/private key pair
        public_key: PEM-encoded public key (required if include_keys)
        private_key: PEM-encoded private key (required if include_keys)
    """
    sw.navigate('security', 'https_cert')
    sw.page.wait_for_timeout(2000)

    sw.page.click("button:has-text('IMPORT CERTIFICATE')")
    sw.page.wait_for_timeout(1500)

    modal = sw.page.query_selector(".modal.show")
    if not modal:
        raise RuntimeError("Import certificate modal not found")

    cert_textarea = modal.query_selector("#txtImportCertificate")
    if cert_textarea:
        cert_textarea.fill(cert_pem)

    if include_keys:
        chk = modal.query_selector("#chckImportRSAKeys")
        if chk and not chk.is_checked():
            sw.page.evaluate("document.getElementById('chckImportRSAKeys').click()")
            sw.page.wait_for_timeout(1000)

        pub_textarea = modal.query_selector("#txtImportPublicKey")
        if pub_textarea and public_key:
            pub_textarea.fill(public_key)

        priv_textarea = modal.query_selector("#txtImportPrivateKey")
        if priv_textarea and private_key:
            priv_textarea.fill(private_key)

    modal.query_selector("#importButtonApply").click()
    sw.page.wait_for_timeout(3000)
    sw.apply_pending()
    return True


def delete_certificate(sw: ArubaSwitch) -> bool:
    """Delete the current HTTPS certificate. Returns True if deleted."""
    sw.navigate('security', 'https_cert')
    sw.page.wait_for_timeout(2000)

    btn = sw.page.query_selector("#btnDeleteCertificate")
    if not btn:
        return False

    btn.click()
    sw.page.wait_for_timeout(2000)
    sw.apply_pending()
    return True