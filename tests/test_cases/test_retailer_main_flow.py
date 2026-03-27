import logging

import allure
import pytest

from tests.data.mock_data import mock_customer_info, mock_vehicle_info, register_mock_info, validate_mock_info
from utils.assert_helper import AssertHelper
from utils.extract import Extract

logger = logging.getLogger()

@allure.epic("TCP API 自动化")
@allure.feature('retailer轮胎注册报损流程测试')
@pytest.mark.usefixtures("retailer_login_info")
class TestRetailerMainFlow:
    """零售商轮胎注册报损流程测试"""

    @pytest.mark.rr
    @allure.story("轮胎注册报损全链路")
    @allure.title("retailer 轮胎注册报损全链路测试")
    @pytest.mark.parametrize(
        "customer_source,vehicle_source",
        [
            ("old", "new"),
            ("old", "old"),
            ("new", "new"),
        ],
        ids=[
            "old_customer_new_vehicle",
            "old_customer_old_vehicle",
            "new_customer_new_vehicle",
        ],
    )
    def test_retailer_tyre_full_flow(self, retailer_main_flow, retailer_login_info, customer_source, vehicle_source):
        """ 全链路测试 retailer 轮胎注册、提交案例、报损校验 """
        retailer = retailer_login_info

        if customer_source == "old":
            customer = mock_customer_info(use_existing=True)
        else:
            customer = mock_customer_info(use_existing=False)

        if vehicle_source == "old":
            try:
                vehicle = mock_vehicle_info(use_existing=True, customer_id=customer.get('id'))
            except ValueError:
                vehicle = mock_vehicle_info(use_existing=False)
        else:
            vehicle = mock_vehicle_info(use_existing=False)
        register_data = register_mock_info()
        validate_data = validate_mock_info()

        retailer_main_flow.set_retailer(retailer)
        
        with allure.step("执行注册轮胎"):
            register_res = retailer_main_flow.register_case(retailer=retailer, customer=customer, vehicle=vehicle, register_data=register_data)
            AssertHelper.assert_json_path(register_res, "code", 0)

        with allure.step("执行轮胎列表，获取item id"):
            vehicle_id = retailer_main_flow.context['vehicle'].get('id')
            itemlist_res = retailer_main_flow.registration_items_case(retailer=retailer, vehicle_id=vehicle_id)
            AssertHelper.assert_json_path(itemlist_res, "code", 0)

        
        with allure.step("执行提交案例"):
            registration_id = retailer_main_flow.context['registration_id']
            item_ids = retailer_main_flow.context['item_ids']
            file_ress = retailer_main_flow.file_case(retailer=retailer, customer=customer, registration_id=registration_id, item_ids=item_ids)
            for file_res in file_ress:
                AssertHelper.assert_json_path(file_res, "code", 0)
        
        with allure.step("执行案例报损校验"):
            case_ids = retailer_main_flow.context['case_ids']
            validate_ress = retailer_main_flow.validate_case(retailer=retailer, customer=customer, case_ids=case_ids, validate_data=validate_data)
            for validate_res in validate_ress:
                AssertHelper.assert_json_path(validate_res, "code", 0)
        
        logger.info("轮胎注册报损全链路测试成功")
