import os
from loguru import logger

from utils.dir_path import CONFIG_DIR
from utils.handle_file import handle_yaml_file


class Environment:
    """环境配置管理类"""
    
    # 单例模式
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Environment, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 避免重复初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        config_file = os.path.join(CONFIG_DIR, 'environment.yaml')
        if not os.path.exists(config_file):
            logger.warning(f"配置文件不存在: {config_file}")
            self.envir = {}
        else:
            self.envir = handle_yaml_file(config_file)
        
        self.env_config = self.envir.get('env', {})
        self.account_config = self.envir.get('account', {})
        self.mysql_config = self.envir.get('mysql', {})
        self._initialized = True

    @staticmethod
    def _as_int(value, fallback):
        """将值转换为整数"""
        if value is None:
            return fallback
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback

    def get_stage_host(self):
        """获取测试环境主机地址"""
        return self.env_config.get('stage_host')

    def get_mysql_config(self):
        """获取MySQL配置"""
        return {
            'host': self.mysql_config.get('host'),
            'port': self._as_int(self.mysql_config.get('port'), None),
            'user': self.mysql_config.get('user'),
            'passwd': self.mysql_config.get('passwd'),
            'db': self.mysql_config.get('db'),
        }
    
    def get_config(self, key, default=None):
        """获取配置项"""
        # 支持点号分隔的嵌套键，如 'env.stage_host'
        keys = key.split('.')
        value = self.envir
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
