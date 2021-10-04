from recon.core.module import BaseModule
import os
import time
from urllib.parse import urlparse


class Module(BaseModule):
    meta = {
        "name": "Github Code Analyzer",
        "author": "j nazario (@jnazario)",
        "description": "Uses the Github API to search for possible vulnerabilites in source code by leveraging Github Dorks and the 'domains' search operator. Updates the 'vulnerabilities' table with the results.",
        "query": "SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL",
        "required_keys": ["github_api"],
        "options": (
            ("sleep", 60, False, "Time to sleep between searches to avoid lockout"),
        ),
        "version": "1.1",
    }

    # via https://www.hackerone.com/blog/how-to-recon-and-content-discovery
    def module_run(self, domains):
        dorks = (
            "secret_key",
            "API_key",
            "aws_key",
            "aws_secret",
            "password",
            "FTP",
            "login",
            "github_token",
        )
        for domain in domains:
            self.heading(domain, level=0)
            for dork in dorks:
                query = "%s %s" % (domain, dork)
                for result in self.search_github_api(query):
                    data = {
                        "host": urlparse(result["html_url"]).netloc,
                        "reference": domain,
                        "example": result["html_url"],
                        "category": dork,
                    }
                    for key in sorted(data.keys()):
                        self.output("%s: %s" % (key.title(), data[key]))
                    self.insert_vulnerabilities(**data)
                    print(self.ruler * 50)
                time.sleep(self.options["sleep"])
