from recon.core.module import BaseModule


class Module(BaseModule):
    meta = {
        "name": "Grayhat Warfare S3 bucket search",
        "author": "J Nazario",
        "description": "Searches for S3 buckets using the GrayhatWarfare API. Updates the 'hosts' table with the results.",
        "query": "SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL",
        "required_keys": [
            "grayhat_warfare",
        ],
        "version": "1.1",
    }

    def module_run(self, domains):
        api_key = self.get_key("grayhat_warfare")
        seen = set()
        for domain in domains:
            keyword = domain.split(".")[-2]  # e.g. adtech.com -> adtech
            if keyword in seen:
                continue
            else:
                seen.add(keyword)
            self.heading(domain, 0)
            url = "https://buckets.grayhatwarfare.com/api/v1/buckets/0/10?access_token={0}&keywords={1}".format(
                api_key, keyword
            )
            data = self.request("GET", url).json()
            for result in data["buckets"]:
                data = {
                    "host": result["bucket"],
                    "reference": "",
                    "example": "",
                    "category": "Amazon AWS S3 bucket exposed",
                }
                self.insert_vulnerabilities(**data)
