import allure

class AssertHelper:

    # @staticmethod
    # def assert_status_code(response, expected_code=200):
    #     with allure.step("断言状态码"):
    #         actual_code = response.status_code
    #         assert actual_code == expected_code, \
    #             f"状态码错误: 实际={actual_code}, 期望={expected_code}"


    @staticmethod
    def assert_json_path(response, path, expected_value):
        with allure.step(f"断言JSON路径: {path}"):
            actual_value = AssertHelper.get_by_path(response, path)

            assert actual_value == expected_value, \
                f"{path}断言失败: 实际={actual_value}, 期望={expected_value}"

    @staticmethod
    def get_by_path(data, path):
        """
        支持 a.b.c 形式
        """
        keys = path.split(".")
        for key in keys:
            data = data.get(key)
            if data is None:
                return None
        return data

    # @staticmethod
    # def assert_text_contains(response, expected_text):
    #     with allure.step("断言文本包含"):
    #         assert expected_text in response.text, \
    #             f"响应中不包含: {expected_text}"

    @staticmethod
    def assert_json_has_key(response, key):
        with allure.step(f"断言字段存在: {key}"):
            assert key in response, f"缺少字段: {key}"