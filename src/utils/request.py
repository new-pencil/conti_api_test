import allure
import requests

from utils.environment import Environment
from utils.logging import Logger

logger = Logger.get_logger()

class Request:
    envir = Environment()
    host = envir.get_stage_host()
    _base_headers = {
        "Content-Type": "application/json",
        "app-ver": "3.0.0",
        "language": "en_MY"
    }
    _token = None

    @classmethod
    def send_request(cls, method, url, **request_data):
        """ 请求封装 """
        request_data.setdefault("timeout", 15)

        # 请求头
        headers = cls._base_headers.copy()
        if cls._token:
            headers["Authorization"] = cls._token
        request_data["headers"] = headers
        
        # 请求信息拆分
        method = method.upper()
        url = cls.host + url
        params = request_data.get("params", None)
        json_data = request_data.get("json", None)

        logger.info(f"【请求】{method} {url} {params}")
        logger.info(f"【headers】{headers}")
        logger.info(f"【请求数据】{json_data}")

        with allure.step(f"{method} {url}"):
            res = requests.request(method, url, **request_data)

            logger.info(f"【响应码】{res.status_code}")
            logger.info(f"【响应体】{res.json()}")

            allure.attach(str(request_data), "请求参数")
            allure.attach(res.json(), "响应结果")

            return res.json()


    @classmethod
    def set_token(cls, token):
        cls._token = token