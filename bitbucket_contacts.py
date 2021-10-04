from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        "name": "Bitbucket Contact Enumerator",
        "author": "j nazario (jnazario)",
        "description": "Uses the Bitbucket API to enumerate users and discover their displayed names. Updates the 'contacts' table with the results.",
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
                name = resp.json()["display_name"].split()
                if len(name) == 1:
                    first_name, middle_name, last_name = name, "", ""
                if len(name) == 2:
                    first_name, middle_name, last_name = (
                        name[0].capitalize(),
                        "",
                        name[1].capitalize(),
                    )
                if len(name) == 3:
                    first_name, middle_name, last_name = (
                        name[0].capitalize(),
                        name[1].capitalize(),
                        name[2].capitalize(),
                    )
                else:
                    first_name, middle_name, last_name = (
                        name[0].capitalize(),
                        " ".join(name[1:-1]).capitalize(),
                        name[-1].capitalize(),
                    )
                self.output("{0} {1} {2}".format(first_name, middle_name, last_name))
                self.insert_contacts(
                    first_name=first_name, middle_name=middle_name, last_name=last_name
                )
