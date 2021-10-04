from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        "name": "CertDB Host Enumeration",
        "author": "Jose Nazario",
        "description": "Uses CertDB to update the 'hosts' and 'contats' tables.",
        "comments": (
            "This module uses the CertDB API to query by organization, parsing TLS ",
            "certificate information to identify hosts and contacts.",
        ),
        "required_keys": ["certdb_key"],
        "query": "SELECT DISTINCT company FROM companies WHERE company IS NOT NULL",
        "version": "1.1",
    }

    def module_run(self, companies):
        companies = {x.lower() for x in companies}
        key = self.get_key("certdb_key")
        for company in companies:
            self.heading(company, level=0)
            resp = self.request(
                "POST",
                "https://certdb.net/api",
                json={
                    "api_key": key,
                    "q": "Organization:%s" % company.replace(" ", "+"),
                },
            )
            if resp.status_code != 200:
                self.error("Error seen with company: {0}".format(company))
                continue
            for cert in resp.json():
                h = cert["subject"].get("CN", None)
                if h:
                    self.insert_hosts(host=h)
                e = cert["subject"].get("emailAddress", None)
                if e:
                    self.insert_contacts(email=e)
