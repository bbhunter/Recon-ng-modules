from recon.core.module import BaseModule
import requests


class Module(BaseModule):
    meta = {
        "name": "Graynoise IP Lookups",
        "author": "Jose Nazario",
        "description": "Uses Graynoise to update the 'domains' table.",
        "comments": ("",),
        "query": "SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL",
        "version": "1.1",
    }

    def module_run(self, hosts):
        domains = set()
        for ip_address in hosts:
            self.heading(ip_address, 1)
            resp = requests.post(
                "http://api.greynoise.io:8888/v1/query/ip", data={"ip": ip_address}
            )
            if resp.json()["status"] == "unknown" or resp.status_code != 200:
                continue
            for r in resp.json()["records"]:
                if len(r["metadata"].get("rdns_parent", "")) > 0:
                    try:
                        domains.add(r["metadata"]["rdns_parent"])
                    except KeyError:
                        pass
        for domain in domains:
            self.insert_domains(domain)
