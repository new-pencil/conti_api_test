import json
import os

import allure
import pytest
from loguru import logger

from common.dir_path import TEST_DATA_DIR
from common.handle_file import handle_yaml_file
from cases.retailer.rmain_case import RMainCase

main_test_case = handle_yaml_file(os.path.join(TEST_DATA_DIR, 'rmain.yaml'))
register = main_test_case['register']
file = main_test_case['file']

@allure.feature('retailer轮胎注册报损主流程')
class TestRMain(RMainCase):
    def _prepare_file_flow(self, register_data, db):
        """复用注册 + file步骤，避免测试方法互相调用。"""
        self.register_case(register_data, db)
        return self.file_case()

    # @pytest.mark.test
    def test_register_tyre(self, register_mock_data, connect_mysql):
        """ 回归测试 retailer register tyre，使用的mock数据"""
        register_data = register_mock_data
        db = connect_mysql
        logger.debug(f"Register Mock Data：{json.dumps(register_data)}")
        with allure.step("执行注册轮胎"):
            res = self.register_case(register_data=register_data, db=db)
        with allure.step("验证注册结果"):
            assert res['code'] == 0
        logger.info(f"轮胎注册用例成功")

    # @pytest.mark.test
    def test_file_case(self, register_mock_data, connect_mysql):
        """ 回归测试 retailer file case，使用的mock数据 """
        register_data = register_mock_data
        db = connect_mysql
        with allure.step("执行案例提交流程"):
            ress = self._prepare_file_flow(register_data=register_data, db=db)
        with allure.step(f"验证 {len(ress)} 条案例提交结果"):
            for i, res in enumerate(ress):
                assert res['code'] == 0
        logger.info(f"file全部成功，一共提交 {len(ress)} 条案例")

    @pytest.mark.test
    def test_validate(self, register_mock_data, validate_mock_data, connect_mysql):
        """ 回归测试 retailer validate，使用的mock数据 """
        db = connect_mysql
        register_data = register_mock_data
        validate_data = validate_mock_data
        with allure.step("准备注册并提交案例"):
            file_results = self._prepare_file_flow(register_data=register_data, db=db)
        with allure.step(f"验证 {len(file_results)} 条案例提交结果"):
            for i, res in enumerate(file_results):
                assert res['code'] == 0
        with allure.step("执行案例提交流程"):
            ress = self.validate_case(validate_data=validate_data)
        with allure.step(f"验证 {len(ress)} 条案例validate结果"):
            for i, res in enumerate(ress):
                assert res['code'] == 0
        logger.info(f"validate全部成功，一共报损 {len(ress)} 条案例")


    @pytest.mark.parametrize('test_case', register)
    def test_register_tyre_full_link(self, test_case, connect_mysql):
        """ 全链路测试 retailer register tyre，使用的参数化 """
        db = connect_mysql
        with allure.step("执行注册轮胎"):
            res = self.register_case(register_data=test_case['data'], db=db)
        with allure.step("验证注册结果"):
            assert test_case['expected']['code'] == res['code']
            assert test_case['expected']['message'] == res['message']
        logger.info(f"轮胎注册用例 {test_case['title']} 成功")




    # @pytest.mark.parametrize('process_test_case', validate_test_case, indirect=True)
    # def test_validate(self, process_test_case):
    #     # 注册轮胎
    #     registration_id, vehicle_id = self._execute_register_flow(process_test_case['register'])
    #
    #     # 获取items
    #     items = self._get_registration_items(registration_id, vehicle_id, 1)
    #
    #     # 提交案例并报损
    #     for item in items:
    #         file_res = self.file_case(registration_id=registration_id, item_id=item)
    #         if file_res['code'] != 0:
    #             pytest.fail(f"item_id为{item}，file case失败")
    #         case_id = file_res["data"]["id"]
    #         res = self.validate(case_id=case_id, datas=process_test_case['data'])
    #         assert process_test_case['expected']['code'] == res['code']
    #         assert process_test_case['expected']['message'] == res['message']
    #
    #     logger.info(f"轮胎保修用例 {process_test_case['title']} 成功 - 验证了{len(items)}个案例")
    #

    #
    # def _get_registration_items(self, registration_id, vehicle_id, status):
    #     items_list_res = self.registration_items(vehicle_id=vehicle_id, status=status)
    #     if items_list_res['code'] != 0:
    #         pytest.fail("items list获取失败")
    #     items = [result['id'] for result in items_list_res["data"]["result"] if
    #              result['customerTyreRegistrationId'] == registration_id]
    #     return items
