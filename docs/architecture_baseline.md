# API 自动化项目最小重构草案

## 1. 目标
在不影响现有用例运行的前提下，先降低耦合和全局状态风险，再逐步重构目录。

## 2. 建议目录（渐进式）
```
api_test/
  apis/                     # 保留当前目录，逐步迁移为 client 层
  cases/                    # 保留当前目录，逐步迁移为 flow/service 层
  testcase/                 # 保留当前测试入口
  config/
  datas/
  docs/
    architecture_baseline.md
```

中期目标：
```
api_test/
  clients/
    retailer/
    customer/
    base_client.py
  services/
    retailer_flow.py
  tests/
    conftest.py
    test_retailer_main.py
  config/
  testdata/
  utils/
```

## 3. 分层职责
- client（原 apis）：只负责 HTTP 调用与响应基础校验，不持有业务流程状态。
- service/flow（原 cases）：编排多接口流程，负责流程上下文。
- test（原 testcase）：断言与数据驱动，不直接拼接复杂业务。

## 4. 当前已落地的最小改造
- `BaseApi.set_auth_headers` 改为返回 headers 副本，避免污染全局 headers。
- `BaseApi.send_request` 改为复制 request data，避免调用方入参被修改。
- `RMainCase.context` 改为实例级初始化，避免类级共享状态。
- `test_validate` 不再调用 `test_file_case`，改为复用步骤函数。

## 5. 下一阶段（建议顺序）
1. 配置治理：将 `config/environment.yaml` 的数据库账号迁移到环境变量，yaml 仅保留占位和非敏感项。
2. client 去硬编码：抽取 accountId/appVersion/os 等公共字段，按角色覆盖差异字段。
3. flow 去继承：`RMainFlow` 使用组合持有 `RMainApi`，避免业务流程与 HTTP 客户端强绑定。
4. 稳定性增强：给关键接口增加 schema 校验和失败重试策略（仅幂等接口）。

## 6. 环境变量键（已支持）
- `API_STAGE_HOST`
- `TEST_RETAILER_ID`
- `TEST_RETAILER_COC`
- `TEST_RETAILER_PHONE`
- `TEST_RETAILER_NAME`
- `TEST_CUSTOMER_ID`
- `TEST_CUSTOMER_PHONE`
- `TEST_CUSTOMER_NAME`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`
