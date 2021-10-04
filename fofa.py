import base64
from urllib.parse import urlencode

import requests

from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        "name": "Fofa Port and Host Enumerator ",
        "author": "Jose Nazario",
        "description": "Queries Fofa using the 'domain' operator to update the 'hosts', and 'ports' tables.",
        "comments": ("",),
        "required_keys": (
            "fofa_email",
            "fofa_key",
        ),
        "query": "SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL",
        "options": (),
        "version": "1.1",
    }

    def module_run(self, domains):
        base_url = "https://fofa.so"
        search_api_url = "/api/v1/search/all"
        fields = "host,ip,port"
        email = self.get_key("fofa_email")
        key = self.get_key("fofa_key")
        for domain in domains:
            param = {
                "qbase64": base64.b64encode(domain),
                "email": email,
                "key": key,
                "page": 1,
                "fields": fields,
            }
            param = urlencode(param)
            url = "%s%s?%s" % (base_url, search_api_url, param)
            resp = self.request("GET", url).json()
            if resp["error"]:
                self.error("Error seen: %s" % resp.json()["errmsg"])
            else:
                print(resp)
