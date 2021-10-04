import re

from recon.core.module import BaseModule
import requests

class Module(BaseModule):
    meta = {
        'name': 'Robtex Passive DNS Lookups',
        'author': 'Jose Nazario',
        'description': 'Uses passive DNS data presented by Robtex to update the \'hosts\' table. Also updates the \'companies\' and \'netblocks\' tables.',
        'query': 'SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL',
        'options': (
            ('restrict', True, True, 'restrict added hosts to current domains'),
        ),
        'version': '1.1',
    }
    
    def module_run(self, hosts):
        # stolen from Recon-ng / modules / recon / hosts-hosts / ssltools.py
        domains = [x[0] for x in self.query('SELECT DISTINCT domain from domains WHERE domain IS NOT NULL')]
        regex = '(?:%s)' % ('|'.join(['\.'+re.escape(x)+'$' for x in domains]))
        for ip_address in hosts:
            self.heading(ip_address, 0)
            url = 'https://freeapi.robtex.com/ipquery/{}'.format(ip_address)            
            resp = self.request('GET', url)
            jsonobj = resp.json()
            if jsonobj['status'] != 'ok':
                self.error(jsonobj['status'])
                continue
            for pa in jsonobj['pas']:
                host = pa['o']
                # apply restriction
                if self.options['restrict'] and not re.search(regex, host):
                    continue
                self.insert_hosts(host)
            self.insert_companies(company=jsonobj['routedesc'])
            self.insert_netblocks(jsonobj['bgproute'])
