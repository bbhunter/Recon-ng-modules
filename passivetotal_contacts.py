from recon.core.module import BaseModule
import requests
from urllib.parse import urlparse
import re


class Module(BaseModule):

    meta = {
        "name": "PassiveTotal Contact Enumerator",
        "author": "j nazario <jose@monkey.org>",
        "description": "Leverages the RiskIQ Passive Total API to list domain contacts based on domains. Updates the 'contacts' table with the results. Requires your account API username and secret, obtain at https://www.passivetotal.org/settings.",
        "required_keys": ["passivetotal_username", "passivetotal_secret"],
        "query": "SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL",
        "version": "1.1",
    }

    def get_passivetotal_whois(self, query, field):
        username = self.get_key("passivetotal_username")
        key = self.get_key("passivetotal_secret")
        auth = (username, key)
        base_url = "https://api.passivetotal.org"
        path = "/v2/whois/search"
        url = base_url + path
        data = {"query": query, "field": field}
        response = requests.get(url, auth=auth, json=data)
        data = response.json()
        res = []
        if not data.get("results", False):
            print(data)
        for result in data.get("results", []):
            try:
                res.append(result["contactEmail"])
            except KeyError:
                pass
        return res

    def module_run(self, domains):
        for domain in domains:
            self.heading(domain, level=0)
            results = self.get_passivetotal_whois(domain, "domain")
            for email in results:
                self.insert_contacts(email=email)
