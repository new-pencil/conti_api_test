import json

from loguru import logger

from utils.request import Request


class CustomerMainApi(Request):
    """customer main apis"""

    def register_api(self, retailer, customer, vehicle, mileage, purchase_photo,
                       purchase_date, tyres):
        url = "/account/3/customer/register/tyre"
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
                "brandName": tyre.get('brand', 'Continental'),
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
        json_data = {
            "accountId": 3,
            "appVersion": "1.9.14.56",
            "comments": "",
            "customerId": customer['id'],
            "customerName": customer['name'],
            "customerVehicleId": vehicle['id'],
            "deviceDetail": "iOS",
            "email": None,
            "inviteCode": "",
            "invoiceNumber": None,
            "mileage": mileage,
            "mileageImage": None,
            "operatorId": customer["id"],
            "operatorType": "CUSTOMER",
            "os": "ios",
            "osVersion": "26.2",
            "phone": customer["phone"],
            "plateNumber": vehicle['plate_number'],
            "proofOfPurchase": purchase_photo,
            "purchaseDate": purchase_date,
            "registrationItems": registration_items,
            "retailerId": retailer["id"],
            "retailerName": retailer["name"],
        }
        res = self.send_request('post', url, json=json_data)
        return res


    def registration_items_api(self, customer, vehicle_id, status=None):
        url = "/account/3/customer/tyre/registration/items"
        json_data = {
            "customerVehicleId": vehicle_id,
            "customerId": customer["id"],
            "status": status
        }
        res = self.send_request('post', url, json=json_data)
        return res


    def file_api(self, customer, retailer, registration_id, item_id):
        url = "/account/3/customer/file/case"
        json_data = {
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
        }
        res = self.send_request('post', url, json=json_data)
        return res

