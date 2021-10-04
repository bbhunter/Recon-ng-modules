from recon.core.module import BaseModule
from recon.mixins.resolver import ResolverMixin
import dns.resolver

class Module(BaseModule, ResolverMixin):

    meta = {
        'name': 'SRV Record Brute Force',
        'author': '@jnazario',
        'description': 'Retrieves commons SRV records for a domain. Updates the \'hosts\' and \'ports\' tables with the results.',
        'comments': (
            'This module reads domains from the domains table and brute forces common ',
            'SRV records associated with each domain. The discovered addresses are ',
            'then stored in the hosts and ports tables.'
        ),
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'version': '1.1',
    }

    def module_run(self, domains):
        # shamelessly stolen from dnsrecon
        # https://github.com/darkoperator/dnsrecon/blob/e8a0941b9bdf1cf94ebacd4d2d85a819ed8f8a79/dnsrecon.py#L344
        srvnames = ('_gc._tcp.', '_kerberos._tcp.', '_kerberos._udp.', '_ldap._tcp.',
        '_test._tcp.', '_sips._tcp.', '_sip._udp.', '_sip._tcp.', '_aix._tcp.',
        '_aix._tcp.', '_finger._tcp.', '_ftp._tcp.', '_http._tcp.', '_nntp._tcp.',
        '_telnet._tcp.', '_whois._tcp.', '_h323cs._tcp.', '_h323cs._udp.',
        '_h323be._tcp.', '_h323be._udp.', '_h323ls._tcp.', '_https._tcp.',
        '_h323ls._udp.', '_sipinternal._tcp.', '_sipinternaltls._tcp.',
        '_sip._tls.', '_sipfederationtls._tcp.', '_jabber._tcp.',
        '_xmpp-server._tcp.', '_xmpp-client._tcp.', '_imap.tcp.',
        '_certificates._tcp.', '_crls._tcp.', '_pgpkeys._tcp.',
        '_pgprevokations._tcp.', '_cmp._tcp.', '_svcp._tcp.', '_crl._tcp.',
        '_ocsp._tcp.', '_PKIXREP._tcp.', '_smtp._tcp.', '_hkp._tcp.',
        '_hkps._tcp.', '_jabber._udp.', '_xmpp-server._udp.', '_xmpp-client._udp.',
        '_jabber-client._tcp.', '_jabber-client._udp.', '_kerberos.tcp.dc._msdcs.',
        '_ldap._tcp.ForestDNSZones.', '_ldap._tcp.dc._msdcs.', '_ldap._tcp.pdc._msdcs.',
        '_ldap._tcp.gc._msdcs.', '_kerberos._tcp.dc._msdcs.', '_kpasswd._tcp.', '_kpasswd._udp.',
        '_imap._tcp.', '_imaps._tcp.', '_submission._tcp.', '_pop3._tcp.', '_pop3s._tcp.',
        '_caldav._tcp.', '_caldavs._tcp.', '_carddav._tcp.', '_carddavs._tcp.',
        '_x-puppet._tcp.', '_x-puppet-ca._tcp.')
        resolver = self.get_resolver()
        for domain in domains:
            for srvname in srvnames:    
                if srvname.endswith('tcp.'): 
                    protocol = 'tcp'
                else: 
                    protocol = 'udp'
                try:
                    answers = resolver.query('%s%s' % (srvname, domain), 'SRV')
                    for record in answers:
                        target = str(record.target).rstrip('.')
                        port = record.port
                        if record.rdtype != 33:
                            continue
                        self.insert_ports(host=target, port=port, protocol=protocol)
                        self.insert_hosts(host=target)
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    self.verbose('%s => No record found.' % ('%s%s' % (srvname, domain)))
                except dns.resolver.Timeout:
                    self.verbose('%s => Request timed out.' % ('%s%s' % (srvname, domain)))
                except (dns.resolver.NoNameservers):
                    self.verbose('%s => Invalid nameserver.' % ('%s%s' % (srvname, domain)))
