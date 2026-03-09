from apis.base_api import BaseApi


class CLoginApi(BaseApi):
    def _sms_send(self):
        customer=BaseApi.test_customer
        data = {
            "method": "post",
            "url": self.host + "/account/sms/send",
            "json": {
                "accessId": "access_id_3",
                "accessKey": "access_key_3",
                "phone": customer["phone"],
            }
        }
        res = self.send_request(data)
        sms_code = res.get("data")
        return sms_code

    def login(self):
        customer=BaseApi.test_customer
        data = {
            "method": "post",
            "url": self.host + "/account/credential/consumer/login",
            "json": {
                "accessId": "access_id_3",
                "accessKey": "access_key_3",
                "code": self._sms_send(),
                "phone": customer["phone"],
            }
        }
        res = self.send_request(data)
        return res

