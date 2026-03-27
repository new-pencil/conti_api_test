import logging
import os
import time

class Logger:
    """
    日志工具类（单例模式）
    作用：
    1. 统一管理日志配置
    2. 同时输出到 控制台 + 文件
    3. 避免重复创建 logger
    """

    _logger = None  # 类变量，用于保存全局唯一 logger 实例

    @staticmethod
    def get_logger():
        """
        获取 logger（单例）
        """

        # 如果已经创建过，直接返回（避免重复初始化）
        if Logger._logger:
            return Logger._logger

        # 创建 logger（名称建议固定，方便统一管理）
        logger = logging.getLogger("api_test")

        # 设置日志级别（DEBUG < INFO < WARNING < ERROR）
        logger.setLevel(logging.DEBUG)

        # 防止重复添加 handler（pytest 多次执行时很关键）
        if not logger.handlers:

            # 定义日志输出格式
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
            )

            # ================= 控制台输出 =================
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.DEBUG)
            logger.addHandler(console_handler)

            # ================= 文件输出 =================
            # 日志目录（不存在则自动创建）
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)

            # 日志文件名（按时间生成，避免覆盖）
            file_name = time.strftime("%Y-%m-%d_%H-%M-%S") + ".log"
            file_path = os.path.join(log_dir, file_name)

            # 文件 handler（指定编码，避免中文乱码）
            file_handler = logging.FileHandler(file_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # 保存 logger 实例（单例）
        Logger._logger = logger

        return logger