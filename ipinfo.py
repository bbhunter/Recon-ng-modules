from recon.core.module import BaseModule
import json
import time


class Module(BaseModule):

    meta = {
        "name": "IPInfo Geolocation",
        "author": "jose nazario",
        "description": "Leverages the ipinfo.io API to geolocate a host by IP address. Updates the 'hosts' table with the results.",
        "required_keys": ["ipinfo_api"],
        "query": "SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL",
        "version": "1.1",
    }

    def module_run(self, hosts):
        api_key = self.get_key("ipinfo_api")
        for host in hosts:
            url = "http://ipinfo.io/%s/json?key=%s" % (host, api_key)
            resp = self.request("GET", url)
            if resp.json:
                jsonobj = resp.json()
            else:
                self.error("Invalid JSON response for '%s'.\n%s" % (host, resp.text))
                continue
            if jsonobj.get("statusCode", "").lower() == "error":
                self.error(jsonobj["statusMessage"])
                continue
            time.sleep(0.7)
            region = (
                ", ".join(
                    [str(jsonobj[x]).title() for x in ["city", "region"] if jsonobj[x]]
                )
                or None
            )
            country = jsonobj["country"].title()
            latitude, longitude = map(str, jsonobj["loc"].split(","))
            self.output(
                "%s - %s,%s - %s"
                % (
                    host,
                    latitude,
                    longitude,
                    ", ".join([x for x in [region, country] if x]),
                )
            )
            self.query(
                "UPDATE hosts SET region=?, country=?, latitude=?, longitude=? WHERE ip_address=?",
                (region, country, latitude, longitude, host),
            )
