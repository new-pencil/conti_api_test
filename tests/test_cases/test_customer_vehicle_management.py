import allure
import pytest

from utils.assert_helper import AssertHelper


@allure.epic("TCP API 自动化")
@allure.feature("Customer Vehicle Management - 流程测试")
@pytest.mark.usefixtures("customer_login_info")
class TestCustomerVehicleFlow:

    @allure.story("车辆管理")
    @allure.title("customer vehicle management flow")
    # @pytest.mark.xxx
    def test_customer_vehicle_management_flow(self, customer_vehicle_flow, customer_login_info, vehicle_mock_data):
        # 获取当前登录的用户信息
        current_customer = customer_login_info
        
        # 设置当前用户到车辆操作流程中
        customer_vehicle_flow.set_customer(current_customer)
        
        # 准备车辆数据
        add_payload = vehicle_mock_data
        update_payload = {
            **add_payload
        }

        with allure.step("新增车辆"):
            add_res = customer_vehicle_flow.add_vehicle_case(customer=current_customer, vehicle_data=add_payload)
            # AssertHelper.assert_status_code(add_res, 200)
            AssertHelper.assert_json_path(add_res, "code", 0)
            # 获取vehicle_id
            vehicle_id = customer_vehicle_flow.context.get("vehicle_id")

        with allure.step("更新车辆"):
            update_res = customer_vehicle_flow.update_vehicle_case(customer=current_customer, vehicle_id=vehicle_id, vehicle_data=update_payload)
            # AssertHelper.assert_status_code(update_res, 200)
            AssertHelper.assert_json_path(update_res, "code", 0)

        with allure.step("删除车辆"):
            delete_res = customer_vehicle_flow.delete_vehicle_case(
                customer=current_customer, 
                vehicle_id=vehicle_id
            )
            # AssertHelper.assert_status_code(delete_res, 200)
            AssertHelper.assert_json_path(delete_res, "code", 0)




