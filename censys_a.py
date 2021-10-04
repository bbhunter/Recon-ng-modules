from recon.core.module import BaseModule
import json

class Module(BaseModule):

    meta = {
        'name': 'Censys.io A Record Retriever',
        'author': 'ScumSec 0x1414',
        'description': 'Retrieves the A records for each host. Updates the \'ports\' table with the results.',
        'query': 'SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL',
        'version': '1.1',
    }

    def module_run(self, hosts):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        base_url = 'https://censys.io/api/v1/search/ipv4'
        for host in hosts:
            self.heading(host, level=0)
            payload = {'query': 'a:%s' % host}
            resp = self.request('POST', base_url, json=payload, auth=(api_id, api_secret))
            # print resp.json
            if resp.status_code == 200:
                pages = resp.json()['metadata']['pages']

                for element in resp.json()['results']:
                    ip_address = element['ip']
                    for protocol in element['protocols']:
                        port, service = protocol.split('/')
                        self.insert_ports(ip_address=ip_address, host=host, port=port, protocol=service)
                if pages > 1:
                    for i in range(pages)[1:]:
                        page_id = i + 1
                        payload = {'page': page_id, 'query': 'a:%s' % host}
                        resp = self.request('POST', base_url, json=payload, auth=(api_id, api_secret))
                        if resp.status_code == 200:
                            for element in resp.json()['results']:
                                ip_address = element['ip']
                                for protocol in element['protocols']:
                                    port, service = protocol.split('/')
                                    self.insert_ports(ip_address=ip_address, host=host, port=port, protocol=service)

            else:
                self.output('%s => Bad request!' % host)
