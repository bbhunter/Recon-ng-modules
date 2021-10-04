import time 

import requests

from recon.core.module import BaseModule

class Module(BaseModule):
    meta = {
        'name': 'ARIN RDAP record enumerator',
        'author': 'Jose Nazario',
        'description': 'Uses networks from the \'netblocks\' table queried to RDAP to update the \'netblocks\' table.',
        'query': 'SELECT DISTINCT netblock FROM netblocks WHERE netblock IS NOT NULL',
        'version': '1.1',
        'comments': (
            'Sleeps 2 seconds between fetches to avoid rate limits',
        ),
    }

    def module_run(self, netblocks):
        for netblock in netblocks:
            self.heading(netblock, level=0)
            net = netblock.strip().split('/')[0]
            url = f'https://rdap.arin.net/registry/ip/{net}'
            data = requests.get(url).json()
            name = data.get('name', None)
            if name != None:
                self.heading(name, level=1)
                self.query('UPDATE netblocks SET notes=? WHERE netblock=?', (name, netblock))
                time.sleep(2)
