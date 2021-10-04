from recon.core.module import BaseModule
import re


class Module(BaseModule):

    meta = {
        "name": "ZoomEye Hostname Enumerator",
        "author": "ScumSec 0x1414",
        "description": "Harvests hosts and ports from the ZoomEye API by using the 'hostname' search operator. Updates the 'hosts' anf the 'ports' tables with the results.",
        "query": "SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL",
        "required_keys": ["zoomeye_key"],
        "version": "1.1",
    }

    def module_run(self, domains):
        access_token = self.get_key("zoomeye_key")
        headers = {"Authorization": "JWT " + access_token}
        for domain in domains:
            self.heading(domain, level=0)
            query = "hostname:%s" % domain
            payload = {"query": query}
            resp = self.request(
                "POST",
                "https://api.zoomeye.org/host/search",
                headers=headers,
                json=payload,
            )
            if resp.status_code == 200:
                if "matches" in resp.json().keys():
                    for match in resp.json()["matches"]:
                        port_info = match["portinfo"]
                        geo_info = match["geoinfo"]
                        host = port_info["hostname"]
                        ip_address = match["ip"]
                        port = port_info["port"]
                        protocol = port_info["service"]
                        region = geo_info["continent"]["names"]["en"]
                        country = geo_info["country"]["names"]["en"]
                        latitude = geo_info["location"]["lat"]
                        longitude = geo_info["location"]["lon"]
                        self.insert_ports(
                            ip_address=ip_address,
                            host=host,
                            port=port,
                            protocol=protocol,
                        )
                        self.insert_hosts(
                            host=host,
                            ip_address=ip_address,
                            region=region,
                            country=country,
                            latitude=latitude,
                            longitude=longitude,
                        )
                else:
                    self.output("%s => No matches!" % domain)
            else:
                self.output("%s => Bad request!" % domain)
