# API 自动化测试框架

## 项目介绍

这是一个基于 Python 的 API 自动化测试框架，用于测试 TCP (Tyre Claim Program) 相关的接口。框架采用分层架构设计，具有良好的可扩展性和可维护性。

## 目录结构

```
api_test/
├── src/                # 源代码目录
│   ├── apis/           # API 层，封装接口请求
│   │   ├── customer/   # 客户相关接口
│   │   ├── retailer/   # 零售商相关接口
│   │   └── base_api.py # 基础 API 类
│   ├── services/       # 业务逻辑层
│   │   ├── customer/   # 客户相关业务逻辑
│   │   └── retailer/   # 零售商相关业务逻辑
│   ├── utils/          # 工具类
│   │   ├── assertion_helper.py  # 断言和数据提取工具
│   │   ├── data_factory.py      # 测试数据生成器
│   │   ├── environment.py       # 环境配置管理
│   │   └── mysql_operate.py     # MySQL 操作工具
│   └── config/         # 配置文件
├── tests/              # 测试目录
│   ├── test_cases/     # 测试用例
│   ├── data/           # 测试数据
│   │   └── mock_data.py # Mock 数据生成
│   └── conftest.py     # 测试 fixtures
├── tokens/             # 存储登录令牌
├── reports/            # 测试报告
├── docs/               # 文档
├── pytest.ini          # pytest 配置文件
└── readme.md           # 项目说明
```

## 核心功能

### 1. 分层架构
- **API层**：封装接口请求，处理 HTTP 请求和响应
- **服务层**：封装业务逻辑，处理接口调用的组合和数据流转
- **测试层**：编写测试用例，验证业务功能

### 2. 测试数据管理
- 支持 Mock 数据生成
- 支持从数据库获取测试数据
- 支持固定池用户数据

### 3. 断言和数据提取
- 封装了丰富的断言方法
- 提供了灵活的数据提取工具
- 支持从响应中提取嵌套字段

### 4. 配置管理
- 集中管理环境配置
- 支持不同环境的切换
- 单例模式，避免重复加载配置

## 技术栈

- **Python 3.9+**
- **pytest**：测试框架
- **requests**：HTTP 客户端
- **allure-pytest**：测试报告生成
- **pymysql**：MySQL 数据库操作
- **Faker**：Mock 数据生成
- **loguru**：日志管理

## 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 配置文件

修改 `src/config/environment.yaml` 文件，配置测试环境：

```yaml
env:
  stage_host: https://conti-tcp-stage.merklechina.com

account:
  test_retailer:
    id: 0
    coc: 0007700236
    phone: 1755555555
    name: SOON LEE HIN_ac
  test_customer:
    id: 1517699
    phone: 1701111117
    name: xiaox

mysql:
  host: 10.22.50.52
  port: 3306
  user: ctcp_dev
  passwd: FyygfXur8gaWlz5d
  db: STG
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_cases/test_retailer_tyre_flow.py -v

# 生成 Allure 报告
pytest --alluredir=reports
allure serve reports
```

## 测试用例

### 1. 零售商轮胎注册报损流程
- `test_register_tyre`：测试轮胎注册功能
- `test_retailer_tyre_full_flow`：测试轮胎注册、提交案例、报损校验全链路

### 2. 客户车辆管理流程
- `test_customer_vehicle_management`：测试客户车辆的增删改查功能

## 核心类和方法

### 1. BaseApi
- `send_request`：发送 HTTP 请求，处理错误和响应
- `set_token`：设置认证令牌

### 2. AssertionHelper
- `assert_success`：断言响应成功
- `assert_batch_success`：断言批量响应成功
- `assert_equal`：断言两个值相等

### 3. DataExtractor
- `extract_field`：从数据中提取字段值
- `extract_vehicle_id`：从响应中提取车辆 ID
- `extract_case_id`：从响应中提取案例 ID

### 4. TestDataManager
- `get_test_data`：从 YAML 文件中获取测试数据
- `get_retailer_tyre_data`：获取零售商轮胎测试数据
- `get_customer_vehicle_data`：获取客户车辆测试数据

## 最佳实践

1. **测试数据管理**：优先使用 Mock 数据，对于需要真实数据的场景，使用数据库查询
2. **断言使用**：使用 `AssertionHelper` 中的断言方法，保持断言风格一致
3. **数据提取**：使用 `DataExtractor` 提取响应数据，避免硬编码路径
4. **错误处理**：利用 BaseApi 中的错误处理机制，确保测试的稳定性
5. **日志管理**：使用 loguru 记录关键操作和错误信息

## 扩展指南

### 1. 添加新的 API

1. 在 `src/apis` 目录下创建新的 API 文件
2. 继承 `BaseApi` 类
3. 实现具体的接口方法

### 2. 添加新的业务流程

1. 在 `src/services` 目录下创建新的服务文件
2. 封装业务逻辑，调用相应的 API
3. 在测试用例中使用服务类

### 3. 添加新的测试用例

1. 在 `tests/test_cases` 目录下创建新的测试文件
2. 编写测试方法，使用 pytest 装饰器
3. 调用服务类的方法，使用 `AssertionHelper` 进行断言

## 注意事项

1. 确保配置文件中的数据库连接信息正确
2. 首次运行测试时，会自动登录并生成令牌文件
3. 测试报告默认生成在 `reports` 目录下
4. 如需修改测试数据，可编辑 `tests/data` 目录下的文件

## 许可证

MIT
