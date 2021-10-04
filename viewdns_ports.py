import urllib

import requests

from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        "name": "ViewDNS Port Enumerator",
        "author": "Jose Nazario",
        "description": "Queries ViewDNS using the 'host' operator to update the 'ports' table.",
        "comments": ("",),
        "required_keys": ("viewdns_key",),
        "query": "SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL",
        "options": (),
        "version": "1.1",
    }

    # http://viewdns.info/api/docs/port-scanner.php

    def module_run(self, hosts):
        key = self.get_key("viewdns_key")
        base_url = "https://api.viewdns.info/portscan/"
        for host in hosts:
            self.heading(host, level=0)
            params = {"key": key, "host": host, "output": "json"}
            params = urlencode(params)
            url = "%s?%s" % (base_url, params)
            resp = self.request("GET", url)
            if resp.status_code != 200 or resp.json is None:
                continue
            resp = resp.json()
            for info in resp["respose"]["port"]:
                if info["status"] != "open":
                    continue
                self.insert_ports(
                    host=host, port=info["number"], protocol=info["service"].lower()
                )
