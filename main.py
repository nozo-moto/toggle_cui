import urllib.request, json
from pytz import timezone
from datetime import datetime
import base64
import settings

class Toggle:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.header = {
            "Content-Type" : "application/json",
            'Authorization': "Basic {}".format(
                self.encode_password_base64(password=self.api_token)
            )
        }

    def encode_password_base64(self, password: str):
        return base64.b64encode(
            '{}:api_token'.format(password).encode('utf-8')
        ).decode('utf-8')

    def send_request(self, url: str, method: str, header: dict, data):
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers=header,
        )
        print(req.data, req.full_url, req.header_items())
        with urllib.request.urlopen(req) as res:
            response_body = res.read()
        return response_body

    def format_dict_to_json(self, data: dict):
        return json.dumps(data).encode("utf-8")

    def start_toggle(self, description: str, tag: list, pid: int):
        url = "https://www.toggl.com/api/v8/time_entries/start"
        data = {
            "time_entry":{
                "description":description,
                "tags":tag,
                "created_with":"python",
            }
        }
        self.send_request(
            url=url,
            method="POST",
            data=self.format_dict_to_json(data),
            header=self.header
        )

def now_time()-> str:
    now_time = datetime.now(
        timezone('UTC')).astimezone(timezone('Asia/Tokyo')
    )
    now_time_str = now_time.strftime("%Y-%m-%dT%H:%M:%S")
    jst_data_un_formated = list(now_time.strftime('%z'))
    jst_data_formated ="{}:{}".format(
        "".join(jst_data_un_formated[0:3]),
        "".join(jst_data_un_formated[3:5])
    )
    return now_time_str + jst_data_formated


if __name__ == '__main__':
    tg = Toggle(settings.ACCSES_TOKEN)
    tg.start_toggle(
        description='APITEST',
        tag=["billed"],
        pid=123,
    )