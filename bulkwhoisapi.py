from recon.core.module import BaseModule

class Module(BaseModule):
    meta = {
        'name': 'Bulk Whois Lookup',
        'author': 'J Nazario (@jnazrio)',
        'description': 'Uses the BulkWhoisAPI to discover contacts from domain names. Updates the "contact" table.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'required_keys': ['bulkwhoisapi_key'],
        'version': '1.1',
    }

    def module_run(self, domains):
        api_key = self.get_key('bulkwhoisapi_key')
        for domain in domains:
            self.heading(domain, level=0)
            url = 'http://api.bulkwhoisapi.com/whoisAPI.php?domain={0}&token={1}'.format(domain, api_key)
            resp = self.request('GET', url)
            if resp.json:
                jsonobj = resp.json()
                print(jsonobj)
            else:
                self.error('Invalid JSON response for \'%s\'.\n%s' % (domain, resp.text))
            data = jsonobj['formatted_data']
            for k,v in data.iteritems():
                if 'email' in k.lower():
                    self.insert_contacts(email=v)
