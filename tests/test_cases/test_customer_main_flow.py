import allure
import pytest

from apis.customer.customer_vehicle_api import CustomerVehicleApi
from tests.data.mock_data import mock_retailer_info, mock_vehicle_info, register_mock_info
from utils.assert_helper import AssertHelper
from utils.extract import Extract
from utils.logging import Logger

logger = Logger.get_logger()

@allure.epic("TCP API 自动化")
@allure.feature('customer轮胎注册报损流程测试')
@pytest.mark.usefixtures("customer_login_info")
class TestCustomerMainFlow:
    """客户轮胎注册报损流程测试"""

    @pytest.mark.cr
    @allure.story("轮胎注册报损全链路")
    @allure.title(f"customer 轮胎注册报损全链路")
    @pytest.mark.parametrize(
        "vehicle_source",
        ["old", "new"],
        ids=["old_vehicle", "new_vehicle"],
    )
    def test_customer_main_flow(self, customer_main_flow, customer_login_info, vehicle_source):
        """ 全链路测试 customer 轮胎注册、提交案例 """
        customer = customer_login_info
        retailer = mock_retailer_info()
        if vehicle_source == "old":
            vehicle = mock_vehicle_info(use_existing=True, customer_id=customer.get("id"))
        else:
            vehicle_init = mock_vehicle_info(use_existing=False)
            add_vehicle_res = CustomerVehicleApi().add_vehicle_api(customer=customer, vehicle=vehicle_init)
            AssertHelper.assert_json_path(add_vehicle_res, "code", 0)
            vehicle_id = Extract.extract_json(add_vehicle_res, "data.id")
            vehicle = {
                **vehicle_init,
                "id": vehicle_id,
            }

        register_data = register_mock_info()

        customer_main_flow.set_customer(customer)
        
        with allure.step("执行注册轮胎"):
            register_res = customer_main_flow.register_case(customer=customer, retailer=retailer, vehicle=vehicle, register_data=register_data)
            # AssertHelper.assert_status_code(register_res, 200)
            AssertHelper.assert_json_path(register_res, "code", 0)
            registration_id = customer_main_flow.context.get("registration_id")
        
        with allure.step("执行提交案例"):
            item_ids = customer_main_flow.context.get("item_ids")
            file_ress = customer_main_flow.file_case(customer=customer, retailer=retailer, registration_id=registration_id, item_ids=item_ids)
            for file_res in file_ress:
                # AssertHelper.assert_status_code(file_res, 200)
                AssertHelper.assert_json_path(file_res, "code", 0)
