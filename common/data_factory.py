import random
import string
from datetime import datetime, timedelta


class DataFactory:

    @classmethod
    def generate_plate_number(cls) -> str:
        """ 生成随机车牌号 3位大写字母 + 4位随机数字"""
        start = ''.join(random.choices(string.ascii_uppercase, k=3))
        end = f"{random.randint(0, 9999):04d}"
        plate_number = f"{start}{end}"
        return plate_number

    @classmethod
    def generate_phone_number(cls) -> str:
        """ 生成随机手机号 1 开头 + 8位数字"""
        phone = f"1{''.join(random.choices(string.digits, k=8))}"
        return phone

    @classmethod
    def generate_purchase_date(cls) -> str:
        """ 生成随机购买日期 限制在当前日期前7天"""
        days_ago = random.randint(0, 6)
        purchase_date = datetime.now() - timedelta(days_ago)
        return purchase_date.strftime("%Y-%m-%d")


    # 固定池
    TYRE_PATTERN = [
        "SportContact 7", "ComfortContact CC5", "UltraContact UC6 SUV"
    ]
    TYRE_SECTION = [195, 200, 205, 210, 215]
    TYRE_ASPECT = [40, 45, 50, 55, 60, 65]
    TYRE_RIM = [15, 16, 17, 18, 19, 20]
    MANU_MODEL = {
        2001: [8001, 8002, 8003, 8004, 8005, 8006, 8007],
        2058: [8578, 8579, 8580],
        2095: [8996, 8997, 8998, 8999, 9000, 9001, 9002],
        2120: [9274, 9275, 9276, 9277, 9278, 9279, 9280, 9281],
    }


    @classmethod
    def generate_pattern(cls) -> str:
        """ 从固定池随机获取一个pattern """
        return random.choice(cls.TYRE_PATTERN)

    @classmethod
    def generate_section(cls) -> str:
        """ 从固定池随机获取一个section """
        return random.choice(cls.TYRE_SECTION)

    @classmethod
    def generate_aspect(cls) -> str:
        """ 从固定池随机获取一个aspect """
        return random.choice(cls.TYRE_ASPECT)

    @classmethod
    def generate_rim(cls) -> str:
        """ 从固定池随机获取一个rim """
        return random.choice(cls.TYRE_RIM)

    @classmethod
    def generate_manu_model(cls) -> tuple[int, int]:
        """ 从固定池随机获取一对 manufacture model """
        manu = random.choice(list(cls.MANU_MODEL.keys()))
        model = random.choice(cls.MANU_MODEL[manu])
        return manu, model



    # @classmethod
    # def generate_tyre_info(cls, tyre_count: int, template_tyres: list) -> list:
    #     """ 补充tyre的信息 pattern section aspect rim"""
    #     tyres = []
    #     barcodes = []
    #     for i in range(tyre_count):
    #         # 保证 template_tyre 是一个dict
    #         if i < len(template_tyres) and isinstance(template_tyres[i], dict):
    #             template_tyre = template_tyres[i]
    #         else:
    #             template_tyre = {}
    #         # 防止单次注册轮胎barcode重复
    #         while True:
    #             barcode = template_tyre.get('barcode', f"111111111{random.randint(0, 9)}")
    #             if barcode not in barcodes:
    #                 barcodes.append(barcode)
    #                 break
    #         # 补充每条barcode数据
    #         tyre = {
    #             "barcode": barcode,
    #             "dot": template_tyre.get('dot', f"1AF{random.randint(100, 999):03d}RY"),
    #             "dot_week": template_tyre.get('dot_week', f"{random.randint(20, 52)}{random.randint(20, 24)}"),
    #             "pattern": template_tyre.get('pattern', random.choice(cls.TYRE_PATTERN)),
    #             "section": template_tyre.get('section', random.choice(cls.TYRE_SECTION)),
    #             "aspect": template_tyre.get('aspect', random.choice(cls.TYRE_ASPECT)),
    #             "rim": template_tyre.get('rim', random.choice(cls.TYRE_RIM))
    #         }
    #         tyres.append(tyre)
    #     return tyres
    #
    # @classmethod
    # def process_register_data(cls, template: dict) -> dict:
    #     """ 组合retailer注册轮胎的测试数据 """
    #     full = dict()
    #     # 处理基础数据
    #     full['plate_number'] = template.get('plate_number', cls.generate_plate_number())
    #     full['manufacture_id'] = 2011
    #     full['model_id'] = 24856
    #     full['company_car'] = template.get('company_car', random.choice([True, False]))
    #     full['mileage'] = template.get('mileage', f"{random.randint(1, 99999999)}")
    #     full['purchase_date'] = template.get('purchase_date', cls.generate_purchase_date())
    #     full['purchase_photo'] = "https://d32iiblykc5ytf.cloudfront.net/case/20251218/bd704e7f-4b2e-4b26-bd51-3008e88b42ca.jpg"
    #
    #     # 处理轮胎信息
    #     template_tyres = template.get('tyres', [])
    #     tyre_count = len(template_tyres)
    #     if tyre_count == 0:
    #         tyre_count = random.randint(2, 4)
    #     full['tyres'] = cls.generate_tyre_info(tyre_count, template_tyres)
    #
    #     return full
