from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        "name": "WhoXY Domain Enumeration",
        "author": "Jose Nazario",
        "description": "Uses WhoXY to update the 'domains' and 'company' tables.",
        "comments": (
            "This module uses the WhoXY API to query by contact email ",
            "information to identify other domain names they have registered.",
        ),
        "required_keys": ["whoxy_key"],
        "query": "SELECT DISTINCT email FROM contacts WHERE email IS NOT NULL",
        "version": "1.1",
    }

    def module_run(self, emails):
        api_key = self.get_key("whoxy_key")
        url = "http://api.whoxy.com/?key={0}&reverse=whois&email={1}"
        for email in emails:
            resp = self.request("GET", url.format(api_key, email))
            if resp.status_code == 200:
                for domain in resp.json()["search_result"]:
                    # add people and addresses too
                    self.insert_domains(domain["domain_name"])
                    company = domain["techical_contact"].get("company_name", None)
                    if company:
                        self.insert_companies(company=company)
