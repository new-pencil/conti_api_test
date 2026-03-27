import os

# 项目根目录
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 配置目录
CONFIG_DIR = os.path.join(PROJECT_DIR, 'src', 'config')
# 令牌目录
TOKENS_DIR = os.path.join(PROJECT_DIR, 'tokens')
# 测试数据目录
TEST_DATA_DIR = os.path.join(PROJECT_DIR, 'tests', 'data')