from recon.core.module import BaseModule

import feedparser
import requests


class Module(BaseModule):

    meta = {
        "name": "crt.sh Certificate Transparency log analyzer",
        "author": "jose nazario @jnazario",
        "description": "Retrieves subdomains using crt.sh, searching through Certificate Transparency logs. Updates the hosts table.",
        "query": "SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL",
        "version": "1.1",
    }

    def module_run(self, domains):
        base_url = "https://crt.sh/atom?q=%25.{}"
        new_domains = set()
        for domain in domains:
            self.heading(domain, 0)
            results = requests.get(base_url.format(domain)).content
            entries = feedparser.parse(results)["entries"]

            line_breaks = ["<br>", "<br />"]
            for entry in entries:
                for cur_break in line_breaks:
                    if cur_break in entry["summary"]:
                        entries_raw = entry["summary"][
                            : entry["summary"].index(cur_break)
                        ].replace("&nbsp;", "\n")
                for e in entries_raw.split("\n"):
                    new_domains.add(str(e.strip()))
        map(self.insert_hosts, filter(lambda x: not x.startswith("*"), new_domains))
