#!/usr/bin/env python3
"""
Aruba Instant On 1930 Switch API
Reusable automation for web GUI operations via Playwright.
"""
import os
import re
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

CRED_FILE = os.path.join(os.path.dirname(__file__), '..', "cred.txt")


def get_creds(cred_file: str = None):
    """Read credentials from a key=value file.

    The file should contain lines like:
        aruba_user=your_username
        aruba_pwd=your_password

    Lines starting with # are ignored.

    Args:
        cred_file: Path to credentials file. Defaults to aruba/cred.txt
                   relative to this module.

    Returns:
        Tuple of (username, password).
    """
    if cred_file is None:
        cred_file = CRED_FILE
    cred_vars = {}
    with open(cred_file) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                cred_vars[k.strip()] = v.strip()
    return cred_vars.get('aruba_user'), cred_vars.get('aruba_pwd')


class ArubaSwitch:
    """Base class for Aruba 1930 switch automation."""

    FOLDER_MAP = {
        'setup': '#folder_1020',
        'switching': '#folder_1070',
        'spanning_tree': '#folder_1140',
        'vlan': '#folder_1200',
        'neighbor_discovery': '#folder_1310',
        'routing': '#folder_1380',
        'qos': '#folder_1430',
        'security': '#folder_1460',
        'diagnostics': '#folder_1560',
        'maintenance': '#folder_1660',
    }

    ITEM_MAP = {
        # Setup Network
        'get_connected': '#item_1020_1030',
        'system_time': '#item_1020_1040',
        'user_management': '#item_1020_1050',
        'schedule_config': '#item_1020_1370',
        # Switching
        'port_config': '#item_1070_1080',
        'port_mirroring': '#item_1070_1090',
        'loop_protection': '#item_1070_1100',
        'igmp_snooping': '#item_1070_1110',
        'snmp': '#item_1070_1120',
        'interface_auto_recovery': '#item_1070_1130',
        'trunk_config': '#item_1070_1300',
        'eee_config': '#item_1070_1550',
        # Spanning Tree
        'stp_global': '#item_1140_1150',
        'cst_config': '#item_1140_1170',
        'mstp_config': '#item_1140_1160',
        # VLAN
        'vlan_config': '#item_1200_1210',
        'voice_vlan': '#item_1200_1220',
        # Neighbor Discovery
        'lldp': '#item_1310_1320',
        'lldp_med': '#item_1310_1330',
        # Routing
        'routing_config': '#item_1380_1390',
        'dhcp_relay': '#item_1380_1410',
        'arp_table': '#item_1380_1420',
        # QoS
        'acl': '#item_1430_1440',
        'cos': '#item_1430_1450',
        # Security
        'radius': '#item_1460_1480',
        'port_access_control': '#item_1460_1490',
        'port_security': '#item_1460_1500',
        'protected_ports': '#item_1460_1510',
        'dhcp_snooping': '#item_1460_1520001',
        'arp_attack_protection': '#item_1460_1530',
        'dos_protection': '#item_1460_1470',
        'https_cert': '#item_1460_1540',
        # Diagnostics
        'logging': '#item_1560_1570',
        'ping': '#item_1560_1580',
        'traceroute': '#item_1560_1590',
        'support_file': '#item_1560_1610',
        'cable_test': '#item_1560_1615',
        'mac_table': '#item_1560_1630',
        'rmon': '#item_1560_1650',
        # Maintenance
        'dual_image': '#item_1660_1670',
        'backup_update': '#item_1660_1680',
        'config_ops': '#item_1660_1690',
        'reset': '#item_1660_1600',
    }

    def __init__(self, ip, page: Page, cred_file: str = None):
        """Create an ArubaSwitch instance.

        Args:
            ip: Switch IP address.
            page: Playwright Page instance.
            cred_file: Path to credentials file. Defaults to aruba/cred.txt
                       relative to this module.
        """
        self.ip = ip
        self.page = page
        self.username, self.password = get_creds(cred_file)

    def login(self):
        """Log into the switch web UI."""
        self.page.goto(f"http://{self.ip}", wait_until="commit", timeout=15000)
        self.page.wait_for_timeout(2000)
        text = self.page.inner_text("body")
        if "LOGIN" in text:
            self.page.fill("input[name='inputUsername']", self.username)
            self.page.fill("input[name='inputPassword']", self.password)
            self.page.wait_for_timeout(500)
            self.page.click("text=LOGIN", timeout=5000)
            self.page.wait_for_url("**/home.htm", timeout=15000)

    def navigate(self, folder: str, item: str):
        """Navigate to a page by folder and item names (keys from FOLDER_MAP/ITEM_MAP).

        Args:
            folder: key from FOLDER_MAP (e.g. 'switching', 'vlan')
            item: key from ITEM_MAP (e.g. 'port_config', 'vlan_config')
        """
        folder_sel = self.FOLDER_MAP[folder]
        item_sel = self.ITEM_MAP[item]

        folder_el = self.page.locator(f"a[href='{self.FOLDER_MAP[folder]}']")
        item_el = self.page.locator(f"a[href='{self.ITEM_MAP[item]}']")

        # Only click folder if items are not visible (folder is collapsed)
        if not item_el.is_visible():
            folder_el.click(timeout=10000)
            self.page.wait_for_timeout(1500)

        item_el.click(timeout=10000)
        self.page.wait_for_timeout(4000)

    def apply_pending(self):
        """Click the page-level Apply button if pending changes exist."""
        btn = self.page.query_selector("#btnApply")
        if btn and btn.is_visible():
            btn.click()
            self.page.wait_for_timeout(3000)
            return True
        return False

    def download_config(self):
        """Download the running config as text."""
        return self.page.evaluate("""
            async () => {
                const r = await fetch(window.location.origin + '/hpe/http_download?action=2&ssd=4', {
                    credentials: 'include'
                });
                return await r.text();
            }
        """)

    def get_firmware_version(self):
        """Return firmware version string from dashboard."""
        self.navigate('maintenance', 'dual_image')
        body = self.page.inner_text("body")
        m = re.search(r'v?InstantOn_?1930[_\s]?(\d+\.\d+\.\d+(?:\.\d+)?)', body)
        return m.group(1) if m else None

    def get_help(self, topic=None):
        """Extract OLH content from the current page.

        The switches embed help as CDATA in <script id="olh..."> tags.
        Help is loaded globally on every page, so navigation is not required.

        Args:
            topic: If provided, return only the help entry matching this string
                   (case-insensitive). If None, return all help entries.

        Returns:
            dict mapping topic_id -> html content (CDATA wrapper stripped).
        """
        # OLH scripts load dynamically, wait for them
        self.page.wait_for_timeout(5000)
        help_scripts = self.page.evaluate("""
            () => {
                const result = {};
                document.querySelectorAll('script[id^="olh"]').forEach(s => {
                    let text = s.textContent;
                    if (text.startsWith('<![CDATA[')) text = text.slice(9);
                    if (text.endsWith(']]>')) text = text.slice(0, -3);
                    result[s.id] = text;
                });
                return result;
            }
        """)

        if topic is None:
            return help_scripts

        topic_lower = topic.lower()
        for aid, html in help_scripts.items():
            if topic_lower in aid.lower():
                return {aid: html}
            if f'"{topic}"' in html.lower() or topic_lower in html[:500].lower():
                return {aid: html}

        return {}

    def list_help_topics(self):
        """Return list of available help topic IDs on the current page.

        Note: OLH scripts load dynamically, so this waits 5s before querying.
        """
        self.page.wait_for_timeout(5000)
        return self.page.evaluate("""
            () => {
                const result = [];
                document.querySelectorAll('script[id^="olh"]').forEach(s => {
                    result.push(s.id);
                });
                return result;
            }
        """)


def connect(ip: str, cred_file: str = None) -> ArubaSwitch:
    """Factory: create a new ArubaSwitch instance, launch browser, and log in.

    Args:
        ip: Switch IP address.
        cred_file: Path to credentials file. Defaults to aruba/cred.txt
                   relative to this module.

    Returns:
        ArubaSwitch instance with authenticated page.

    Caller is responsible for closing browser when done.
    """
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        ignore_https_errors=True,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        viewport={'width': 1920, 'height': 1080}
    )
    page = context.new_page()
    sw = ArubaSwitch(ip, page, cred_file)
    sw.login()
    sw._browser = browser
    sw._context = context
    sw._playwright = p
    return sw


def disconnect(sw: ArubaSwitch):
    """Close browser and cleanup."""
    sw._context.close()
    sw._browser.close()
    sw._playwright.stop()
