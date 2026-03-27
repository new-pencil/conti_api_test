import pytest
import sys
import os
import shutil

TEST_PATH = "tests/test_cases"
ALLURE_DATA = "reports/allure_data"
ALLURE_HTML = "reports/html"

args = sys.argv[1:]

pytest_args = ["-vs", TEST_PATH, f"--alluredir={ALLURE_DATA}"]

mark = None
path = None

# ===== 解析参数（超简版）=====
i = 0
while i < len(args):
    if args[i] == "-m":
        mark = args[i + 1]
        i += 2
    else:
        path = args[i]
        i += 1

# ===== 应用参数 =====
if path:
    if os.path.exists(path):
        pytest_args[1] = path

if mark:
    pytest_args.extend(["-m", mark])

# ===== 清理报告 =====
if os.path.exists(ALLURE_DATA):
    shutil.rmtree(ALLURE_DATA)

if os.path.exists(ALLURE_HTML):
    shutil.rmtree(ALLURE_HTML)

print(f"🚀 path: {path}")
print(f"🏷️ mark: {mark}")

# ===== 执行 =====
pytest.main(pytest_args)

# ===== 报告 =====
os.system(f"allure generate {ALLURE_DATA} -o {ALLURE_HTML} --clean")
os.system(f"allure open {ALLURE_HTML}")