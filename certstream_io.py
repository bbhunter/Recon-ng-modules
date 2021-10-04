from recon.core.module import BaseModule
import re
import time

import certstream

class Module(BaseModule):

    meta = {
        'name': 'Certstream',
        'author': 'ScumSec 0x1414',
        'description': 'Parses the Certstream data for certificate transparency updates, listening for updates matching the domain. Updates the \'domains\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'comments': (
            'Because the Certstream data is never ending, this only listens for 1000 records a run.',
        ),
        'version': '1.1',
    }

    def module_run(self, domains):
        pat = re.compile(".*\.({})$".format('|'.join(domains)))
        new_domains = []

        def _cb(message, context):
            c = context.get('count', 0)
            context.count = c + 1
            if context.count > 1000:
                raise KeyboardInterrupt
            new_domains.append(message['data']['leaf_cert']['all_domains'])

        try:
            certstream.listen_for_events(_cb)
        except (StopIteration, KeyboardInterrupt):
            for new_domain in new_domains:
                self.insert_domains(new_domain)
