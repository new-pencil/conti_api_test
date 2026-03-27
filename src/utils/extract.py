import re
from utils.logging import Logger

logger = Logger.get_logger()

class Extract:

    @staticmethod
    def extract_json(data, path):
        """
        支持：
        - a.b.c
        - data.list[0].id

        :param response:
        :param path:
        :return:
        """

        try:
            # 拆路径：a.list[0].id → ['a', 'list[0]', 'id']
            parts = path.split(".")

            for part in parts:
                # 匹配 list[0]
                match = re.match(r"(\\w+)\\[(\\d+)\\]", part)

                if match:
                    key = match.group(1)
                    index = int(match.group(2))

                    data = data.get(key)[index]
                else:
                    data = data.get(part)

                if data is None:
                    logger.warning(f"提取失败，字段不存在: {path}")
                    return None

            logger.info(f"【数据提取】{path} = {data}")
            return data

        except Exception as e:
            logger.error(f"提取异常: {path}，错误: {e}")
            return None