import json
import socket
import time

import requests

from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        "name": "Farsight pDNS record enumerator",
        "author": "Jose Nazario",
        "description": "Uses IP addresses from the 'hosts' table to query the Farsight passive DNS repository for known hostnames",
        "query": "SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL AND module != \"farsight_ip\"",
        "required_keys": ["farsight_key"],
        "version": "1.1",
    }

    def module_run(self, ips):
        api_key = self.get_key("farsight_key")
        for ip in ips:
            try:
                socket.inet_aton(ip)
            except OSError:
                continue
            self.heading(ip, level=0)
            url = f"https://api.dnsdb.info/dnsdb/v2/lookup/rdata/ip/{ip}"
            headers = {"X-API-Key": api_key,
                       'Accept': 'application/x-ndjson',
                      }
            text = requests.get(url, headers=headers).text
            for line in text.splitlines():
                # avoid stuff like CNAME or NS records that wound up in there
                try:
                    data = json.loads(line)
                except:
                    # TODO - enumerate FSI errors
                    self.error(line)
                    return
                if not data.get('obj', False):
                    continue
                if data['obj'].get('rrtype', 'NO') in ('A', 'AAAA'):
                    host = data['obj'].get('rrname', '').rstrip('.')
                    ip_addresses = data['obj'].get('rdata', '')
                    notes = time.asctime(time.gmtime(int(data['obj'].get('time_last', 0))))
                    for address in ip_addresses: 
                        self.insert_hosts(host=host, ip_address=address, notes=notes)
