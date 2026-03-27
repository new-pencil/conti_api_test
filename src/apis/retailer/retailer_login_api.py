from utils.request import Request


class RetailerLoginApi(Request):
    def _sms_send(self, retailer_phone):
        url = "/account/sms/send"
        json_data = {
            "accessId": "access_id_3",
            "accessKey": "access_key_3",
            "phone": retailer_phone
        }
        res = self.send_request('post', url, json=json_data)
        sms_code = res.get("data")
        return sms_code

    def login(self, retailer_phone):
        url = "/account/credential/retailer/login"
        json_data = {
            "accessId": "access_id_3",
            "accessKey": "access_key_3",
            "appVersion": "3.9.14.56",
            "code": self._sms_send(retailer_phone),
            "deviceDetail": "iOS",
            "os": "ios",
            "osVersion": "17.5",
            "phone": retailer_phone
        }
        res = self.send_request('post', url, json=json_data)
        return res
