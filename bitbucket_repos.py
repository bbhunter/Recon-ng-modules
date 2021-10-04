from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        "name": "Bitbucket Repository Enumerator",
        "author": "j nazario (jnazario)",
        "description": "Uses the Bitbucket API to enumerate repositories and snippets owned by a Bitbucket user. Updates the 'repositories' table with the results.",
        "query": "SELECT DISTINCT username FROM profiles WHERE username IS NOT NULL AND resource LIKE 'Bitbucket'",
        "version": "1.1",
    }

    def module_run(self, users):
        for user in users:
            self.heading(user, level=0)
            resp = self.request(
                "GET", "https://bitbucket.org/api/2.0/users/{}".format(user)
            )
            if resp.status_code == 200:
                self.heading("Repositories", level=1)
                repos = self.request(
                    "GET", resp.json()["links"]["repositories"]["href"]
                )
                if repos.status_code == 200:
                    for repo in repos.json["values"]:
                        data = {
                            "name": repo["name"],
                            "owner": repo["owner"]["username"],
                            "description": repo["description"],
                            "url": repo["website"],
                            "resource": "Bitbucket",
                            "category": "repo",
                        }
                        self.output("%s - %s" % (repo["name"], repo["description"]))
                        self.insert_repositories(**data)
                self.heading("Snippets", level=1)
                snippets = self.request("GET", resp.json()["links"]["snippets"]["href"])
                if snippets.status_code == 200:
                    for snippet in snippets.json["values"]:
                        # TODO
                        pass
