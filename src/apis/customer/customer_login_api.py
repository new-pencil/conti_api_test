from utils.request import Request


class CustomerLoginApi(Request):
    """ customer login api """
    def _sms_send(self, customer_phone):
        """ 发送短信 """
        url = "/account/sms/send"
        json_data = {
            "accessId": "access_id_3",
            "accessKey": "access_key_3",
            "phone": customer_phone
        }
        res = self.send_request('post', url, json=json_data)
        sms_code = res.get("data")
        if not sms_code:
            raise ValueError(f"sms send api没有返回的sms_code，返回{res}")
        return sms_code

    def login(self, customer_phone):
        """ customer login api """
        url = "/account/credential/consumer/login"
        json_data = {
            "accessId": "access_id_3",
            "accessKey": "access_key_3",
            "code": self._sms_send(customer_phone),
            "phone": customer_phone
        }
        res = self.send_request('post', url, json=json_data)
        return res
