import os

import pytest

from services.retailer.retailer_main_flow import RetailerMainFlow
from utils.request import Request
from apis.customer.customer_login_api import CustomerLoginApi
from apis.retailer.retailer_login_api import RetailerLoginApi
from services.customer.customer_main_flow import CustomerMainFlow
from services.customer.customer_vehicle_flow import CustomerVehicleFlow
# from services.retailer.retailer_main_flow import RetailerMainFlow
from utils.dir_path import TOKENS_DIR
from utils.mysql_operate import MysqlOperate
from tests.data.mock_data import (
    mock_customer_info,
    mock_retailer_info
)


# 登录相关fixture
@pytest.fixture(scope="class")
def retailer_login_info():
    """获取零售商登录信息和token"""
    retailer = mock_retailer_info()
    if not retailer:
        return None
    
    # 从文件中获取token，没有时存入
    token_file = os.path.join(TOKENS_DIR, f"retailer_{retailer['phone']}.txt")
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            token = f.read().strip()
    else:
        token = RetailerLoginApi().login(retailer_phone=retailer['phone'])["data"]["token"]
        with open(token_file, "w") as f:
            f.write(token)
    
    # 将token存入请求头
    Request().set_token(token)
    
    # 返回当前登录的零售商信息
    return retailer


@pytest.fixture(scope="class")
def customer_login_info():
    """获取客户登录信息和token"""
    # 获取用户
    customer = mock_customer_info(use_existing=True)
    if not customer:
        return None
    
    # 从文件中获取token，没有时存入
    token_file = os.path.join(TOKENS_DIR, f"customer_{customer['phone']}.txt")
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            token = f.read().strip()
    else:
        login_res = CustomerLoginApi().login(customer_phone=customer['phone'])
        token = login_res["data"]["token"]
        # 从响应中提取用户id并更新customer对象
        if login_res.get("data") and login_res["data"].get("customer"):
            customer_id = login_res["data"]["customer"].get("id")
            if customer_id:
                customer["id"] = customer_id
        with open(token_file, "w") as f:
            f.write(token)
    
    # 将token存入请求头
    Request().set_token(token)
    
    # 返回当前登录的用户信息
    return customer


# 业务流程fixture
@pytest.fixture()
def retailer_main_flow():
    """零售商轮胎注册报损流程"""
    return RetailerMainFlow()


@pytest.fixture()
def customer_vehicle_flow():
    """客户车辆管理流程"""
    return CustomerVehicleFlow()


@pytest.fixture()
def customer_main_flow():
    """客户轮胎注册报损流程"""
    return CustomerMainFlow()


# 数据库fixture
@pytest.fixture(scope="session")
def connect_mysql():
    """连接MySQL数据库"""
    db = MysqlOperate()
    yield db
    db.close_connection()
