from recon.core.module import BaseModule


class Module(BaseModule):

    meta = {
        "name": "DNSTrails data miner",
        "author": "jose nazario @jnazario",
        "description": "Retrieves hosts sharing the same IP from the DNSTrails data set. Updates the 'hosts' and `domains` tables. This is an unauthenticated use of their API and is rate limited.",
        "query": "SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL",
        "version": "1.1",
    }

    def _fmt_hostname(self, host, domain):
        if host is not none:
            return "{}.{}".format(host, domain)
        else:
            return domain

    def module_run(self, ips):
        for ip in ips:
            self.heading(ip, level=0)
            url = "https://app.securitytrails.com/api/search/by_type/ip/{}".format(ip)
            try:
                resp = self.request(url)
                if resp.status_code == 200:
                    hosts = map(
                        lambda x: self._fmt_hostname(x["host"], x["domain"]),
                        resp.json()["result"]["items"],
                    )
                    domains = set([x["domain"] for x in resp.json()["result"]["items"]])
                    for host in hosts:
                        self.insert_hosts(host=host, ip_address=ip)
                    for domain in domains:
                        self.insert_domains(domain)
            except:
                self.error("Error received. Try again later, API limits probably hit.")
