import json

import pytest
import requests
from loguru import logger

from Utils.environment import Environment


class BaseApi:
    envir = Environment()
    host = envir.get_stage_host()
    _base_headers = {
        "Content-Type": "application/json",
        "app-ver": "3.0.0",
        "language": "en_MY"
    }
    test_customer = envir.get_test_customer()
    test_retailer = envir.get_test_retailer()
    _token = None

    @classmethod
    def send_request(cls, data):
        """
        封装请求
        :param data: 请求数据
        :return:
        """
        request_data = data.copy()
        request_data['headers'] = cls.set_auth_headers()
        try:
            res = requests.request(**request_data)
        except Exception as e:
            logger.error(f"请求参数 {request_data}")
            logger.exception(f"请求异常 {e}")
            raise e
        else:
            logger.info(f"请求成功：{res.status_code}")
            logger.info(f"响应时间: {res.elapsed.total_seconds():.2f}秒")
            try:
                return res.json()
            except json.JSONDecodeError as e:
                logger.error(f"响应不是JSON: status={res.status_code}, text={res.text}")
                raise e

    @classmethod
    def set_token(cls, token):
        cls._token = token

    @classmethod
    def set_auth_headers(cls):
        headers = cls._base_headers.copy()
        if cls._token:
            headers["Authorization"] = cls._token
        return headers

    @classmethod
    def extract_info_from_response(cls, response, keys_path: dict):
        """
        从返回中提取数据
        Args:
            response: API 返回，json格式
            key_path: dict 定义了需要的返回值
                     例如: {'registration_id': ['data', 'customerTyreRegistrationId'],
                           'vehicle_id': ['data', 'customerVehicleId']}
        Returns:
            一个包含提取结果的字典。
        Raises:
            AssertionError: 如果任何必需的key不存在或code不为0。
        """
        # 检查响应状态码
        assert response['code'] == 0, \
            f"API调用失败，响应{response}"

        # 根据keys_path提取数据
        extract = {}
        try:
            for var_name, key_path in keys_path.items():
                value = response
                for key in key_path:
                    value = value.get(key, None)
                extract.update({var_name: value})
        except (KeyError, TypeError, IndexError) as e:
            pytest.fail(f"从响应中提取失败！路径: {keys_path}. "
                        f"响应结构可能已更改。原始响应: {response}. 错误: {e}")
        return extract



