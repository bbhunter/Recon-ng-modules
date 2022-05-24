mkdir -p ~/.recon-ng/modules/import
cp nmap_xml.py ~/.recon-ng/modules/import
cp theharvester_xml.py ~/.recon-ng/modules/import
cp simplyemail_json.py ~/.recon-ng/modules/import

mkdir -p ~/.recon-ng/modules/recon/companies-contacts
cp vk_companies.py ~/.recon-ng/modules/recon/companies-contacts
cp xing_employees.py ~/.recon-ng/modules/recon/companies-contacts

mkdir -p ~/.recon-ng/modules/recon/domains-contacts
cp vk_news.py ~/.recon-ng/modules/recon/domains-contacts
cp email_format.py ~/.recon-ng/modules/recon/domains-contacts
cp emailhunter.py ~/.recon-ng/modules/recon/domains-contacts
cp bulkwhoisapi.py ~/.recon-ng/modules/recon/domains-contacts
cp passivetotal_contacts.py ~/.recon-ng/modules/recon/domains-contacts
cp dnssoa.py ~/.recon-ng/modules/recon/domains-contacts

mkdir -p ~/.recon-ng/modules/recon/companies-hosts
cp shodan_org.py ~/.recon-ng/modules/recon/companies-hosts
# cp censys_org.py ~/.recon-ng/modules/recon/companies-hosts

mkdir -p ~/.recon-ng/modules/recon/contacts-credentials
cp hacked_emails.py  ~/.recon-ng/modules/recon/contacts-credentials

mkdir -p ~/.recon-ng/modules/recon/contacts-domains
cp passivetotal_domains.py ~/.recon-ng/modules/recon/contacts-domains
cp whoxy.py ~/.recon-ng/modules/recon/contacts-domains

mkdir -p ~/.recon-ng/modules/recon/contacts-profiles
cp vibeapp.py ~/.recon-ng/modules/recon/contacts-profiles
cp migrate_contacts.py ~/.recon-ng/modules/recon/contacts-profiles

mkdir -p ~/.recon-ng/modules/recon/domains-hosts
cp baidu_site.py ~/.recon-ng/modules/recon/domains-hosts
cp axfr.py ~/.recon-ng/modules/recon/domains-hosts
cp mx-ip.py ~/.recon-ng/modules/recon/domains-hosts
cp spf-ip.py ~/.recon-ng/modules/recon/domains-hosts
cp threatcrowd_api.py ~/.recon-ng/modules/recon/domains-hosts
# cp censys_mx.py ~/.recon-ng/modules/recon/domains-hosts
cp zoomeye_hostname.py ~/.recon-ng/modules/recon/domains-hosts
cp dnsdumpster-query.py ~/.recon-ng/modules/recon/domains-hosts
cp crt_sh.py ~/.recon-ng/modules/recon/domains-hosts
cp passivetotal_subdomains.py ~/.recon-ng/modules/recon/domains-hosts
cp virustotal.py ~/.recon-ng/modules/recon/domains-hosts

mkdir -p ~/.recon-ng/modules/recon/hosts-companies
cp otx_pulse_host.py ~/.recon-ng/modules/recon/hosts-companies

mkdir -p ~/.recon-ng/modules/recon/hosts-netblocks
cp arin.py ~/.recon-ng/modules/recon/hosts-netblocks

mkdir -p ~/.recon-ng/modules/recon/domains-domains
cp threatcrowd_domain.py ~/.recon-ng/modules/recon/domains-domains
cp certstream_io.py ~/.recon-ng/modules/recon/domains-domains
cp spyonweb_analytics.py ~/.recon-ng/modules/recon/domains-domains
cp spyonweb_adsense.py ~/.recon-ng/modules/recon/domains-domains
cp crt_sh.py ~/.recon-ng/modules/recon/domains-domains
cp nsec_walker.py ~/.recon-ng/modules/recon/domains-domains

mkdir -p ~/.recon-ng/modules/recon/domains-vulnerabilities
cp github_secrets.py ~/.recon-ng/modules/recon/domains-vulnerabilities/
cp grayhat.py ~/.recon-ng/modules/recon/domains-vulnerabilities/

mkdir -p ~/.recon-ng/modules/recon/hosts-domains
cp otx_pulse_hostname.py ~/.recon-ng/modules/recon/hosts-domains
cp greynoise.py ~/.recon-ng/modules/recon/hosts-domains
cp psl_migrate.py ~/.recon-ng/modules/recon/hosts-domains

mkdir -p ~/.recon-ng/modules/recon/domains-ports
cp fofa.py ~/.recon-ng/modules/recon/domains-ports

mkdir -p ~/.recon-ng/modules/recon/hosts-ports
# cp censys_a.py ~/.recon-ng/modules/recon/hosts-ports
# cp censys_ip.py ~/.recon-ng/modules/recon/hosts-ports
cp viewdns_ports.py ~/.recon-ng/modules/recon/hosts-ports

mkdir -p ~/.recon-ng/modules/recon/hosts-hosts
cp farsight_ip.py ~/.recon-ng/modules/recon/hosts-hosts
cp ipinfo.py ~/.recon-ng/modules/recon/hosts-hosts
cp dnstrails.py ~/.recon-ng/modules/recon/hosts-hosts
cp otx_pulse_ip.py   ~/.recon-ng/modules/recon/hosts-hosts
cp otx_pulse_pdns.py ~/.recon-ng/modules/recon/hosts-hosts
cp robtex.py ~/.recon-ng/modules/recon/hosts-hosts
cp srvbrute.py ~/.recon-ng/modules/recon/hosts-hosts
cp zoomeye_ip.py ~/.recon-ng/modules/recon/hosts-hosts

mkdir -p ~/.recon-ng/modules/recon/netblocks-netblocks
cp rdap.py ~/.recon-ng/modules/recon/netblocks-netblocks

mkdir -p ~/.recon-ng/modules/recon/netblocks-hosts
cp zoomeye_net.py ~/.recon-ng/modules/recon/netblocks-hosts

mkdir -p ~/.recon-ng/modules/recon/profiles-repositories
cp bitbucket_repos.py ~/.recon-ng/modules/recon/profiles-repositories

mkdir -p ~/.recon-ng/modules/recon/profiles-contacts
cp bitbucket_contacts.py ~/.recon-ng/modules/recon/profiles-contacts

mkdir -p ~/.recon-ng/modules/recon/profiles-profiles
cp bitbucket_profile.py ~/.recon-ng/modules/recon/profiles-profiles

# probes are direct contact with the host to assess vulns
mkdir -p ~/.recon-ng/modules/probe/hosts-vulnerabilities/
# cp tls_analyze.py  ~/.recon-ng/modules/probe/hosts-vulnerabilities/

for key in `echo "bulkwhoisapi_key
emailhunter_key
fofa_email
fofa_key
grayhat_warfare
ipinfo_api
spyonweb_secret
vibeapp_key
viewdns_key
vk_key
whoxy_key
zoomeye_key"`; do
	echo "INSERT INTO keys (name) VALUES (\"$key\");" | sqlite3 ~/.recon-ng/keys.db
done
