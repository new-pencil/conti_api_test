import json

from loguru import logger

from apis.base_api import BaseApi


class CMainApi(BaseApi):
    """customer main apis"""

    def c_register_api(self, retailer, vehicle, company_car, mileage, purchase_photo,
                       purchase_date, tyres, manufacturer_id=2001, model_id=8002):
        # 用户信息
        customer = BaseApi.test_customer
        # items信息
        registration_items = []
        for i, tyre in enumerate(tyres):
            item = {
                "articleCode": "03113770000",
                "dotWeek": "0126",
                "initalMileage": mileage,
                "internalProductId": None,
                "origin": "MY",
                "plantCode": "1AF",
                "productAspect": tyre['aspect'],
                "productDot": "1AF0327RY",
                "productId": tyre["barcode"],
                "productPattern": tyre["pattern"],
                "productRim": tyre["rim"],
                "productSection": tyre["section"],
                "serialNumberImage": "",
                "wheelPostion": str(i + 1)
            }
            registration_items.append(item)
        # 请求体完整信息
        payload = {
            "method": "POST",
            "url": f"{self.host}/account/3/customer/register/tyre",
            "json": {
                "accountId": 3,
                # "address": "",
                "appVersion": "1.9.14.56",
                # "city": "",
                "comments": "",
                # "companyCar": company_car,
                "customerId": customer['id'],
                "customerName": customer['name'],
                "customerVehicleId": vehicle['id'],
                "deviceDetail": "iOS",
                "email": None,
                "inviteCode": "",
                "invoiceNumber": None,
                # "manufacturerId": manufacturer_id,
                "mileage": mileage,
                "mileageImage": None,
                # "modelId": model_id,
                "operatorId": retailer["id"],
                "operatorType": "RETAILER",
                "os": "ios",
                "osVersion": "26.2",
                "phone": customer["phone"],
                "plateNumber": vehicle['plate_number'],
                # "postalCode": "",
                "proofOfPurchase": purchase_photo,
                "purchaseDate": purchase_date,
                "registrationItems": registration_items,
                "retailerId": retailer["id"],
                "retailerName": retailer["name"],
            }
        }
        logger.info(f"开始发送customer注册轮胎请求 plate_number {vehicle['plate_number']}")
        logger.info(f"请求参数:+++++++++ {json.dumps(payload)}")
        res = self.send_request(payload)
        logger.info(f"注册轮胎接口的返回是: ========== {json.dumps(res)}")
        return res


    def c_registration_items_api(self, vehicle_id, status=None):
        customer=BaseApi.test_customer
        payload = {
            "method": "POST",
            "url": f"{self.host}/account/3/customer/tyre/registration/items",
            "json": {
                "customerVehicleId": vehicle_id,
                # "retailerId": retailer["id"],
                "customerId": customer["id"],
                "status": status
            }
        }
        logger.info(f"开始发送items list请求")
        logger.info(f"请求参数:+++++++++ {json.dumps(payload)}")
        res = self.send_request(payload)
        logger.debug(f"items list接口的返回是:========== {json.dumps(res)}")
        return res


    def c_file_api(self, registration_id, item_id, retailer):
        customer = BaseApi.test_customer
        payload = {
            "method": "POST",
            "url": f"{self.host}/account/3/customer/file/case",
            "json": {
                "accountId": 3,
                "appVersion": "1.9.14.56",
                "customerId": customer["id"],
                "deviceDetail": "iOS",
                "operatorId": customer["id"],
                "operatorType": "CUSTOMER",
                "os": "ios",
                "osVersion": "26.2",
                "programeName": None,
                "registrationId": registration_id,
                "registrationItemId": item_id,
                "retailerId": retailer["id"]
                # "status": 1
            }
        }
        logger.info(f"开始发送customer file case请求")
        logger.info(f"请求参数:+++++++++++++ {json.dumps(payload)}")
        res = self.send_request(payload)
        logger.debug(f"customer file case接口的返回是:============ {json.dumps(res)}")
        logger.info(f"item_id为 {item_id} 的轮胎file成功")
        return res


