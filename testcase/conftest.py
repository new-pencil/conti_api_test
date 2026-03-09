import os

import pytest

from common.mysql_operate import MysqlOperate
from testcase.mock_data import register_mock_info, validate_mock_info
from apis.base_api import BaseApi
from apis.retailer.rlogin_api import RLoginApi
from common.dir_path import TOKENS_DIR



@pytest.fixture(scope="class", autouse=True)
def retailer_login_token():
    # 从文件中获取token，没有时存入
    retailer = BaseApi.test_retailer
    token_in = os.path.join(TOKENS_DIR, f"{retailer['phone']}.txt")
    if os.path.exists(token_in):
        with open(token_in, "r") as f:
            token = f.read().strip()
    else:
        token = RLoginApi().login()["data"]["token"]
        with open(token_in, "w") as f:
            f.write(token)
    # 将token存入请求头
    BaseApi().set_token(token)


@pytest.fixture()
def register_mock_data():
    return register_mock_info()

@pytest.fixture()
def validate_mock_data():
    return validate_mock_info()


@pytest.fixture(scope="session")
def connect_mysql():
    db = MysqlOperate()
    yield db
    db.close_connection()
#
# @pytest.fixture()
# def process_test_case(request):
#     param = request.param
#     req = {
#         'title': param['title'],
#         'expected': param['expected']
#     }
#     # 处理注册数据
#     if 'register' in param:
#         req['register'] = RegisterFactory.process_register_data(param['register'])
#
#     # 处理其他数据
#     if 'data' in param:
#         req['data'] = param['data']
#
#     return req
#
#
# @pytest.fixture()
# def raw_test_case(request):
#     param = request.param
#     return param
