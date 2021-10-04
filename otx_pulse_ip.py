from recon.core.module import BaseModule

class Module(BaseModule):

    meta = {
        'name': 'OTX Pulse Enumerator',
        'author': 'j nazario (@jnazario)',
        'description': 'Leverages the OTX Pulse API to enumerate other virtual hosts sharing the same IP address. Updates the \'hosts\' and \'domains\' table with the results.',
        'query': 'SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL',
        'version': '1.1',
    }

    def module_run(self, hosts):
        for host in hosts:
            self.heading(host, level=0)
            url = 'https://otx.alienvault.com/api/v1/indicators/IPv4/{0}/passive_dns'.format(host)
            resp = self.request('GET', url)
            jsonobj = resp.json
            for hostname in [x['hostname'] for x in jsonobj['passive_dns']]:
                self.insert_hosts(hostname, host)
                self.output('\'%s\' successfully found.' % (hostname))

            url = 'https://otx.alienvault.com/api/v1/indicators/IPv4/{0}/url_list'.format(host)
            resp = self.request('GET', url)
            jsonobj = resp.json
            for url in jsonobj['url_list']:
                self.insert_domains(domain=url['domain'])
                self.output('\'%s\' successfully found.' % (url['domain']))
                self.insert_hosts(url['hostname'], host)
                self.output('\'%s\' successfully found.' % (url['hostname']))

