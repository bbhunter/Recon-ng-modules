from recon.core.module import BaseModule

# from recon.utils.parsers import parse_hostname
from urllib.parse import urlparse
import requests
import re


class Module(BaseModule):

    meta = {
        "name": "Passive Total Subdomains Enumerator",
        "author": "Vlad Styran (@c2FwcmFu)",
        "description": "Leverages the RiskIQ Passive Total API to list DNS subdomains. Updates the 'hosts' table with the results. Requires your account API username and secret, obtain at https://www.passivetotal.org/settings.",
        "required_keys": ["passivetotal_username", "passivetotal_secret"],
        "query": "SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL",
        "version": "1.1",
    }

    def query_passivetotal_api(self, path, query):
        username = self.get_key("passivetotal_username")
        key = self.get_key("passivetotal_secret")
        auth = (username, key)
        base_url = "https://api.passivetotal.org"
        url = base_url + path
        data = {"query": query}
        response = requests.get(url, auth=auth, json=data)
        return response.json()

    def get_passivetotal_subdomains(self, query):
        pdns_results = self.query_passivetotal_api("/v2/enrichment/subdomains", query)
        results = []
        for subdomain in pdns_results["subdomains"]:
            results.append(subdomain + "." + query)
        return results

    def module_run(self, domains):
        for domain in domains:
            self.heading(domain, level=0)
            hosts = []
            results = []
            results = self.get_passivetotal_subdomains(domain)
            for host in results:
                if host.endswith("." + domain) and host not in hosts:
                    hosts.append(host)
                    self.insert_hosts(host)
