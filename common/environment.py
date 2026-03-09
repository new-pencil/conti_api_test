import os

from common.dir_path import CONFIG_DIR
from common.handle_file import handle_yaml_file


class Environment:

    def __init__(self):
        config_file = os.path.join(CONFIG_DIR, 'environment.yaml')
        self.envir = handle_yaml_file(config_file) if os.path.exists(config_file) else {}
        self.env_config = self.envir.get('env', {})
        self.account_config = self.envir.get('account', {})
        self.mysql_config = self.envir.get('mysql', {})

    @staticmethod
    def _as_int(value, fallback):
        if value is None:
            return fallback
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback

    def get_stage_host(self):
        return os.getenv('API_STAGE_HOST', self.env_config.get('stage_host'))

    def get_test_retailer(self):
        yaml_retailer = self.account_config.get('test_retailer', {})
        return {
            'id': self._as_int(os.getenv('TEST_RETAILER_ID'), yaml_retailer.get('id')),
            'coc': os.getenv('TEST_RETAILER_COC', yaml_retailer.get('coc')),
            'phone': os.getenv('TEST_RETAILER_PHONE', yaml_retailer.get('phone')),
            'name': os.getenv('TEST_RETAILER_NAME', yaml_retailer.get('name')),
        }

    def get_test_customer(self):
        yaml_customer = self.account_config.get('test_customer', {})
        return {
            'id': self._as_int(os.getenv('TEST_CUSTOMER_ID'), yaml_customer.get('id')),
            'phone': os.getenv('TEST_CUSTOMER_PHONE', yaml_customer.get('phone')),
            'name': os.getenv('TEST_CUSTOMER_NAME', yaml_customer.get('name')),
        }

    def get_mysql_config(self):
        return {
            'host': os.getenv('MYSQL_HOST', self.mysql_config.get('host')),
            'port': self._as_int(os.getenv('MYSQL_PORT'), self.mysql_config.get('port')),
            'user': os.getenv('MYSQL_USER', self.mysql_config.get('user')),
            'passwd': os.getenv('MYSQL_PASSWORD', self.mysql_config.get('passwd')),
            'db': os.getenv('MYSQL_DB', self.mysql_config.get('db')),
        }
