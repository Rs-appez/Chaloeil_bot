import config
import httpx


class EcoCraft:
    api_url: str = config.BACKEND_URL + "almanax/api/economy-entries/"

    headers: dict[str, str] = {"Authorization": config.BACKEND_TOKEN}

    def __init__(self, job: str):
        self.job = job

    def get_date(self):
        res: httpx.Response = httpx.get(
            self.api_url + "get_job/", params={"job": self.job}, headers=self.headers
        )
        data = res.json()
        return (data.get("day"), data.get("month"))

    @staticmethod
    def get_all_dates():
        res: httpx.Response = httpx.get(EcoCraft.api_url, headers=EcoCraft.headers)
        res_json = res.json()
        data = []
        data.extend(res_json.get("results", []))
        while res_json.get("next", None):
            res = httpx.get(res_json["next"], headers=EcoCraft.headers)
            res_json = res.json()
            data.extend(res_json.get("results", []))
        return [
            (entry.get("bonus"), entry.get("day"), entry.get("month")) for entry in data
        ]
