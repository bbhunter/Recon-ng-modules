from recon.core.module import BaseModule
import requests
import re

class Module(BaseModule):

    meta = {
        'name': 'PassiveTotal Domain Enumerator',
        'author': 'j nazario <jose@monkey.org>',
        'description': 'Leverages the RiskIQ Passive Total API to list DNS domain based no contact emails. Updates the \'domains\' table with the results. Requires your account API username and secret, obtain at https://www.passivetotal.org/settings.',
        'required_keys': ['passivetotal_username', 'passivetotal_secret'],
        'query': 'SELECT DISTINCT email FROM contacts WHERE email IS NOT NULL',
        'version': '1.1',
        }

    def get_passivetotal_whois(self, query, field):
        username = self.get_key('passivetotal_username')
        key = self.get_key('passivetotal_secret')
        auth = (username, key)
        base_url = 'https://api.passivetotal.org'
        path = '/v2/whois/search?field={0}'.format(field)
        url = base_url + path
        data = {'query': query, 'field': field}
        response = requests.get(url, auth=auth, json=data)
        data = response.json()
        res = []
        if not data.has_key('results'):
            self.error(data)
        for result in data.get('results', []):
            res.append(result['domain'])
        return res

    def module_run(self, emails):
        for email in emails:
            self.heading(email, level=0)
            results = self.get_passivetotal_whois(email, 'email')
            for domain in results:
                self.insert_domains(domain)
