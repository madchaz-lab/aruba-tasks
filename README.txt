Aruba Instant On 1930 Switch Automation
=======================================

A reusable Python API for automating Aruba Instant On 1930 switches (JL682A)
through their web GUI using Playwright.

These switches only support web-based management (no SSH, no CLI, no REST API),
so all operations are performed by automating a headless Chromium browser.

Dependencies
------------
  - Python 3.10+
  - playwright (install with: pip install playwright && playwright install chromium)

Setup
-----
  1. Create a cred.txt file in the repository root with your switch credentials:

       aruba_user=your_username
       aruba_pwd=your_password

     This file is in .gitignore and will never be committed.

  2. Install dependencies:

       pip install playwright
       playwright install chromium

Usage
-----
  import sys
  sys.path.insert(0, '/path/to/aruba-tasks')
  from tasks import connect, disconnect
  from tasks import vlan, routing, port, trunk, backup

  sw = connect("192.168.27.2")  # switch IP
  vlans = vlan.list_vlans(sw)
  disconnect(sw)

  Or with a custom credentials file:

  sw = connect("192.168.27.2", cred_file="/path/to/my-creds.txt")

Available Modules
-----------------
  tasks (base)  - connect(), disconnect(), ArubaSwitch.navigate(), download_config()
  vlan          - list_vlans(), rename_vlan(), delete_vlan(), add_vlan()
  routing       - list_vlan_interfaces(), clear_vlan_ip(), set_vlan_ip()
  port          - list_ports(), edit_port_pvid(), set_port_description()
  trunk         - list_trunks(), disable_trunk(), clear_trunk_members()
  backup        - backup_config(), get_firmware_info()

Notes
-----
  - Requires Playwright with Chromium installed
  - Switches must be accessible via HTTP on the network
  - Trunk removal is not supported by the web UI; use disable_trunk() + clear_trunk_members()
  - VLAN deletion requires no IP interface or DHCP relay configured on the VLAN

License
-------
  BSD 2-Clause (see LICENSE)
