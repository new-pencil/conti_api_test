import random


from common.data_factory import DataFactory
from faker import Faker

df = DataFactory()
fake = Faker()

def register_mock_info():
    """ 组合retailer注册轮胎的测试数据 """
    full = dict()
    # 车辆信息
    manu, model = df.generate_manu_model()
    full['plate_number'] = df.generate_plate_number()
    full['manufacturer_id'] = manu
    full['model_id'] = model
    full['company_car'] = random.choice([True, False])
    full['mileage'] = random.randint(1, 99999999)

    # 购买信息
    full['purchase_date'] = df.generate_purchase_date()
    full['purchase_photo'] = "https://d32iiblykc5ytf.cloudfront.net/case/20251218/bd704e7f-4b2e-4b26-bd51-3008e88b42ca.jpg"

    # 用户信息
    full['customer_phone'] = df.generate_phone_number()
    full['customer_name'] = fake.name()

    # 处理轮胎信息
    full['tyres'] = _mock_tyres_info()

    return full

def _mock_tyres_info() -> list:
    """ mock tyre info"""
    count = random.randint(2, 4)
    tyres = []
    barcodes = []
    for i in range(count):
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
            "pattern": df.generate_pattern(),
            "section": df.generate_section(),
            "aspect": df.generate_aspect(),
            "rim": df.generate_rim(),
        }
        tyres.append(tyre)
    return tyres


def validate_mock_info():
    """ mock tyre info"""
    full = {}
    tread_depth = random.uniform(5.0, 7.0)
    final_mileage = random.randint(1, 99999999)
    full['tread_depth'] = tread_depth
    full['final_mileage'] = final_mileage
    return full

