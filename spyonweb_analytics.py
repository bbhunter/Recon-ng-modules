from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        'name': 'SpyOnWeb analyzer using Google Analytics identifier',
        'author': 'jose nazario',
        'description': 'Parses the SpyOnWeb data for shared Google Analytics IDs, looking for other domains that share the Google Analytics identifier. Updates the \'domains\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'version': '1.1',
    }
    
    def module_run(self, domains):
        api_secret = self.get_key('spyonweb_secret')
        summary_url = 'https://api.spyonweb.com/v1/summary/{}?access_token={}'
        analytics_url = 'https://api.spyonweb.com/v1/analytics/{}?access_token={}'
        for domain in domains:
            self.heading(domain, 0)
            domainresp = self.request('GET', summary_url.format(domain, api_secret)).json()
            if domainresp['status'] != 'found':
                continue
            analytics = domainresp['result']['summary'][domain]['items'].get('analytics', {})
            for aid in analytics.keys():
                resp = self.request('GET', analytics_url.format(aid, api_secret)).json()
                for k,data in resp['result']['analytics'].iteritems():
                    self.heading(k, 1)
                    for new_domain,date in data['items'].iteritems():
                        self.insert_domains(new_domain)
