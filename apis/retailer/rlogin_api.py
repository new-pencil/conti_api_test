from apis.base_api import BaseApi


class RLoginApi(BaseApi):
    def _sms_send(self):
        retailer=BaseApi.test_retailer
        data = {
            "method": "post",
            "url": self.host + "/account/sms/send",
            "json": {
                "accessId": "access_id_3",
                "accessKey": "access_key_3",
                "phone": retailer["phone"],
            }
        }
        res = self.send_request(data)
        sms_code = res.get("data")
        return sms_code

    def login(self):
        retailer=BaseApi.test_retailer
        data = {
            "method": "post",
            "url": self.host + "/account/credential/retailer/login",
            "json": {
                "accessId": "access_id_3",
                "accessKey": "access_key_3",
                "appVersion": "3.9.14.56",
                "code": self._sms_send(),
                "deviceDetail": "iOS",
                "os": "ios",
                "osVersion": "17.5",
                "phone": retailer["phone"],
            }
        }
        res = self.send_request(data)
        return res

