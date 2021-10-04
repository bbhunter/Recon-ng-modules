from recon.core.module import BaseModule

class Module(BaseModule):
    meta = {
        'name': 'VirusTotal Passive DNS Host Enumeration',
        'author': 'Jose Nazario',
        'description': 'Leverages the VirusTotal Passive DNS service to enumerate other virtual hosts sharing the same IP address. Updates the \'hosts\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'version': '1.1',
    }

    def module_run(self, domains):
        url = 'https://www.virustotal.com/ui/domains/{0}/subdomains?limit=20'
        for domain in domains:
            self.heading(domain, level=0)
            data = self.request('GET', url.format(domain))
            if data.status_code != 200:
                self.error('Error seen with domain: {0}'.format(domain))
                continue
            for result in data.json()['data']:
                self.insert_hosts(host=result['id'])
