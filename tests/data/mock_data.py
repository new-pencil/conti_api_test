from typing import Any
import random

from src.utils.data_factory import DataFactory
from faker import Faker

from src.utils.mysql_operate import MysqlOperate

# 初始化全局对象
df = DataFactory()
fake = Faker()

def mock_customer_info(use_existing):
    """ mock customer info """
    if use_existing:
        #1 从数据库中随机获取一个现有客户
        result = MysqlOperate().query_one(
            "select id, phone, name from customers where account_id = 3 and deleted != 1 order by rand() limit 1"
        )
        if result:
            customer = {
                "id": result['id'],
                "phone": result['phone'],
                "name": result['name']
            }
        else:
            # 2 直接获取固定数据
            customer = {"id": 1517699, "phone": "1701111117", "name": "xiaox"}
            # {"id": 1517699, "phone": "1607700997", "name": "t1"}
    else: 
        # 判断 customer 不在数据库中，如果在数据库中，重新生成新的随机手机号
        while True:
            customer_phone = DataFactory.generate_phone_number()
            result = MysqlOperate().query_one(
                "select id, phone, name from customers where account_id = 3 and phone = %s",
                (customer_phone,)
            )
            if not result:
                break
        customer = {"id": None, "phone": customer_phone, "name": fake.name()}

    return customer

def mock_retailer_info():
    """ mock retailer info """
    retailer = None
    try:
        # 从数据库中随机获取一个零售商
        result = MysqlOperate().query_one(
            "select id, tcp_mobile , tcp_name , retailer_id from retailers where account_id = 3 and participate_status = 3 order by rand() limit 1"
        )
        if result:
            retailer = {
                "id": result['id'],
                "phone": result['tcp_mobile'],
                "name": result['tcp_name'],
                "coc": result['retailer_id']
            }
    except Exception:
        # 如果数据库查询失败，返回默认值
        retailer = {
            "id": 86328,
            "phone": "1755555555",
            "name": "SOON LEE HIN_ac",
            "coc": "0007700236" 
        }
    return retailer

def mock_vehicle_info(use_existing=False, customer_id=None):
    """ mock customer vehicle """
    if use_existing and customer_id:
        # 使用数据库的数据，根据customer从数据库中获取客户的车辆，随机一个
        result = MysqlOperate().query_one(
            "select id, manufacturer_id, manufacturer_name, model_id, model_name, plate_number, company_car from customer_vehicles where account_id = 3 and customer_id = %s order by rand() limit 1",
            (customer_id,)
        )
        if not result:
            raise ValueError("该用户下面没有车辆，请先添加")
        vehicle = {
            "id": result['id'],
            "manufacturer_id": result['manufacturer_id'],
            "model_id": result['model_id'],
            "plate_number": result['plate_number'],
            "model_name": result['model_name'],
            "manufacturer_name": result['manufacturer_name'],
            "company_car": result['company_car']
        }
        # else:
        #     # 如果客户没有车辆，生成新车
        #     manu, model = DataFactory.generate_manu_model()
        #     vehicle = {
        #         "id": None,
        #         "manufacturer_id": manu,
        #         "model_id": model,
        #         "plate_number": DataFactory.generate_plate_number(),
        #         "model_name": None,
        #         "manufacturer_name": None,
        #         "company_car": random.choice([True, False])
        #     }
    else:
        # 生成新车
        manu, model = DataFactory.generate_manu_model()
        # 生成唯一的车牌号
        while True:
            plate_number = DataFactory.generate_plate_number()
            # 检查车牌号是否已存在
            result = MysqlOperate().query_one(
                "select id from customer_vehicles where account_id = 3 and plate_number = %s",
                (plate_number,)
            )
            if not result:
                break
        vehicle = {
            "id": None,
            "manufacturer_id": manu,
            "model_id": model,
            "plate_number": plate_number,
            "model_name": None,
            "manufacturer_name": None,
            "company_car": random.choice([True, False])
        }
    return vehicle

def register_mock_info():
    """ 组合retailer注册轮胎的测试数据 """
    full = dict[Any, Any]()

    # 注册里程信息
    full['mileage'] = random.randint(1, 69999)
    
    # 购买信息
    full['purchase_date'] = DataFactory.generate_purchase_date()
    full['purchase_photo'] = "https://d32iiblykc5ytf.cloudfront.net/case/20251218/bd704e7f-4b2e-4b26-bd51-3008e88b42ca.jpg"

    # 处理轮胎信息
    full['tyres'] = _mock_tyres_info()

    return full

def _mock_tyres_info() -> list:
    """ mock tyre info"""
    count = random.randint(2, 4)
    tyres = []
    barcodes = []
    for _ in range(count):
        # 防止单次注册轮胎barcode重复
        while True:
            barcode = f"111111111{random.randint(0, 9)}"
            if barcode not in barcodes:
                barcodes.append(barcode)
                break
        # 补充每条barcode数据
        tyre = {
            "barcode": barcode,
            "dot": f"1AF{random.randint(100, 999):03d}RY",
            "dot_week": f"{random.randint(20, 52)}{random.randint(20, 24)}",
            "pattern": DataFactory.generate_pattern(),
            "section": DataFactory.generate_section(),
            "aspect": DataFactory.generate_aspect(),
            "rim": DataFactory.generate_rim(),
            "brand": "Continental"
        }
        tyres.append(tyre)
    return tyres


def validate_mock_info():
    """ mock tyre info"""
    full = {}
    tread_depth = random.uniform(5.0, 7.0)
    final_mileage = random.randint(1000, 79999)  # 确保最终里程大于注册里程，且不超过太多
    full['tread_depth'] = tread_depth
    full['final_mileage'] = final_mileage
    return full


