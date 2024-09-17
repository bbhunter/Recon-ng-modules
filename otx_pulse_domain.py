from recon.core.module import BaseModule

class Module(BaseModule):

    meta = {
        "name": "OTX Pulse Domain Enumerator",
        "author": "j nazario (@jnazario)",
        "description": "Leverages the OTX Pulse API to discover hosts for a domain. Updates the 'hosts' table with the results.",
        "query": "SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL",
        "version": "1.1",
    }

    def module_run(self, domains):
        for domain in domains:
            self.heading(domain, level=0)
            url = "https://otx.alienvault.com/api/v1/indicators/domain/{0}/passive_dns".format(
                domain
            )
            resp = self.request("GET", url)
            jsonobj = resp.json()
            if jsonobj.get("Error", False):
                self.error(jsonobj["Error"])
                continue
            for result in jsonobj["passive_dns"]:
                self.insert_hosts(host=result['hostname'], 
                                  ip_address=result['address'],
                                  notes=result.get('asn', ''))
                self.output("'%s' successfully found." % (result['address']))
