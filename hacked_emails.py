from recon.core.module import BaseModule
import time


class Module(BaseModule):

    meta = {
        "name": "Hacked-Email.com Breach Search",
        "author": "ScumSec @0x1414",
        "description": "Leverages the hacked-email.com API to determine if email addresses are associated with breached credentials. Adds compromised email addresses to the 'credentials' table.",
        "query": "SELECT DISTINCT email FROM contacts WHERE email IS NOT NULL",
        "version": "1.1",
    }

    def module_run(self, emails):
        base_url = "https://hacked-emails.com/api"
        for email in emails:
            payload = {"q": email}
            resp = self.request("GET", base_url, json=payload)
            if resp.status_code == 200:
                # if not resp.json()['data']
                leak_info = resp.json()["data"]
                if leak_info:
                    for leak in leak_info:
                        self.alert(
                            "%s => Breach found! Seen in the %s breach that occurred on %s."
                            % (
                                email,
                                leak["title"],
                                leak["date_leaked"].replace("T", " "),
                            )
                        )
                        self.insert_credentials(username=email, leak=leak["title"])
                else:
                    self.verbose("%s => Not Found!" % email)
            else:
                self.output("%s => Bad request!" % email)
            time.sleep(1)
