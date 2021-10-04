from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        'name': 'SpyOnWeb analyzer using Google Adsense identifier',
        'author': 'jose nazario',
        'description': 'Parses the SpyOnWeb data for shared Google Adsense identifiers, looking for other domains that share the Google Adsense identifier. Updates the \'domains\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'version': '1.1',
    }
    
    def module_run(self, domains):
        api_secret = self.get_key('spyonweb_secret')
        summary_url = 'https://api.spyonweb.com/v1/summary/{}?access_token={}'
        adsense_url = 'https://api.spyonweb.com/v1/adsense/{}?access_token={}'
        for domain in domains:
            self.heading(domain, 0)
            domainresp = self.request('GET', summary_url.format(domain, api_secret)).json()
            if domainresp['status'] != 'found':
                continue
            adsense = domainresp['result']['summary'][domain]['items'].get('adsense', {})
            for aid in adsense.keys():
                resp = self.request('GET', adsense_url.format(aid, api_secret)).json()
                for k,data in resp['result']['adsense'].iteritems():
                    self.heading(k, 1)
                    for new_domain,date in data['items'].iteritems():
                        self.insert_domains(new_domain)
