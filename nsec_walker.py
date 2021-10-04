from recon.core.module import BaseModule

import dns.query
import dns.resolver
from dns.resolver import NoAnswer

class Module(BaseModule):

    meta = {
        'name': 'NSEC domain enumeration',
        'author': 'jose nazario @jnazario',
        'description': 'Retrieves subdomains by enumerating DNS zone entries based on DNSSEC NSEC chains.  It can be used to discover hosts in a DNS zone quickly and with a minimum amount of queries if said zone is DNSSEC-enabled. Updates the \'domains\' table.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'version': '1.1',
        }

    def module_run(self, domains):
        allresults = set()

        def trim(domain):
            return domain.rstrip('.')
    
        # https://github.com/anonion0/nsec3map/blob/master/n3map/nsecwalker.py
        for domain in domains:
            self.heading(domain, level=0)
            seen = set()
            seen.add(domain)
            try:
                ans = dns.resolver.query(domain, rdtype='NSEC', tcp=True)
                latest = trim(ans.rrset.items[0].to_text().split()[0])
                self.output('FOUND %s' % latest)
            except NoAnswer:
                self.error("Doesn't support NSEC, trying next domain")
                continue
            while latest not in seen:
                try:
                    ans = dns.resolver.query(latest, rdtype='NSEC', tcp=True)
                except NoAnswer:
                    self.error('Error with NSEC query for %s, moving to next domain' % latest)
                    break
                seen.add(latest)
                latest = trim(ans.rrset.items[0].to_text().split()[0])                
                self.output('FOUND %s' % latest)
            allresults = allresults ^ seen
            [ self.insert_domains(x) for x in allresults ]
