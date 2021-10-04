from recon.core.module import BaseModule
import os
import re


class Module(BaseModule):

    meta = {
        "name": "Contacts to Profiles Data Migrator",
        "author": "Tim Tomes (@LaNMaSteR53)",
        "description": "Coverts from contacts to profiles after using the dev_diver module.",
        "query": 'SELECT DISTINCT first_name, middle_name, last_name, title FROM contacts WHERE title like "% Contributor" AND module = "dev_diver"',
        "version": "1.1",
    }

    def module_run(self, names):
        URLS = {
            "Github Contributor": "https://github.com/%s",
            "Bitbucket Contributor": "https://bitbucket.org/%s",
            "Sourceforge Contributor": "http://sourceforge.net/u/%s/profile/",
            "CodePlex Contributor": "http://www.codeplex.com/site/users/view/%s",
        }

        for name in names:
            fname, mname, lname, title = name
            username = "%s%s%s" % (fname or "", mname or "", lname or "")
            url = URLS[title] % username
            resource = title.split()[0]
            self.heading(f"{name} -> {username}")
            self.insert_profiles(
                username=username, url=url, resource=resource, category=title
            )
