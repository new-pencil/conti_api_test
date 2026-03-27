import json

from loguru import logger

from utils.request import Request


class RetailerMainApi(Request):
    """retailer main apis"""

    def register_api(self, retailer, customer, vehicle, mileage, purchase_photo, purchase_date, tyres):
        url = "/account/3/retailer/register/tyre"
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
            "address": "",
            "appVersion": "1.9.14.56",
            "city": "",
            "comments": "",
            "companyCar": vehicle['company_car'],
            "customerId": customer['id'],
            "customerName": customer['name'],
            "customerVehicleId": vehicle['id'],
            "deviceDetail": "iOS",
            "email": None,
            "inviteCode": "",
            "invoiceNumber": None,
            "manufacturerId": vehicle['manufacturer_id'],
            "mileage": mileage,
            "mileageImage": None,
            "modelId": vehicle['model_id'],
            "operatorId": retailer["id"],
            "operatorType": "RETAILER",
            "os": "ios",
            "osVersion": "26.2",
            "phone": customer["phone"],
            "plateNumber": vehicle['plate_number'],
            "postalCode": "",
            "proofOfPurchase": purchase_photo,
            "purchaseDate": purchase_date,
            "registrationItems": registration_items,
            "retailerId": retailer["id"],
            "retailerName": retailer["name"]
        }
        res = self.send_request('post', url, json=json_data)
        return res


    def registration_items_api(self, retailer, vehicle_id, status=None):
        url = "/account/3/customer/tyre/registration/items"
        json_data = {
            "customerVehicleId": vehicle_id,
            "retailerId": retailer["id"],
            "status": status
        }
        res = self.send_request('post', url, json=json_data)
        return res


    def file_api(self, customer, retailer, registration_id, item_id):
        url = "/account/3/retailer/file/case"
        json_data = {
            "accountId": 3,
            "appVersion": "1.9.14.56",
            "customerId": customer["id"],
            "deviceDetail": "iOS",
            "operatorId": retailer["id"],
            "operatorType": "RETAILER",
            "os": "ios",
            "osVersion": "26.2",
            "registrationId": registration_id,
            "registrationItemId": item_id,
            "retailerId": retailer["id"],
            "status": 1
        }
        res = self.send_request('post', url, json=json_data)
        return res



    def validate_api(self, customer, retailer, case_id, final_mileage, tread_depth):
        url = "/account/3/retailer/validate/case"
        params = {
            "mileage": final_mileage
        }
        json_data = [
                {
                    "appVersion": "1.9.14.56",
                    "coverRetailerId": False,
                    "customAttributes": None,
                    "customerCaseId": case_id,
                    "customerId": customer['id'],
                    "deviceDetail": "iOS",
                    "imageUrl": "https://d32iiblykc5ytf.cloudfront.net/case/20260126/b4b91ae3-b4e4-433d-817e-b2872918e01b.jpg",
                    "mileage": final_mileage,
                    "operatorId": retailer["id"],
                    "operatorType": "RETAILER",
                    "orderIndex": 1,
                    "os": "ios",
                    "osVersion": "26.2",
                    "programId": 101,
                    "programName": "TCP Program",
                    "programRuleId": 1042,
                    "treadDepth": tread_depth
                },
                {
                    "appVersion": "1.9.14.56",
                    "coverRetailerId": False,
                    "customAttributes": None,
                    "customerCaseId": case_id,
                    "customerId": customer['id'],
                    "deviceDetail": "iOS",
                    "imageUrl": "https://d32iiblykc5ytf.cloudfront.net/case/20260126/2d6689d8-b390-4204-8795-0ffa886afc04.jpg",
                    "mileage": final_mileage,
                    "operatorId": retailer["id"],
                    "operatorType": "RETAILER",
                    "orderIndex": 2,
                    "os": "ios",
                    "osVersion": "26.2",
                    "programId": 101,
                    "programName": "TCP Program",
                    "programRuleId": 1046,
                    "treadDepth": tread_depth
                },
                {
                    "appVersion": "1.9.14.56",
                    "coverRetailerId": False,
                    "customAttributes": None,
                    "customerCaseId": case_id,
                    "customerId": customer['id'],
                    "deviceDetail": "iOS",
                    "imageUrl": "https://d32iiblykc5ytf.cloudfront.net/case/20260126/cb22834e-eae5-4d08-b1a8-b5c7b3a10ec0.jpg",
                    "mileage": final_mileage,
                    "operatorId": retailer["id"],
                    "operatorType": "RETAILER",
                    "orderIndex": 3,
                    "os": "ios",
                    "osVersion": "26.2",
                    "programId": 101,
                    "programName": "TCP Program",
                    "programRuleId": 1044,
                    "treadDepth": tread_depth
                },
                {
                    "appVersion": "1.9.14.56",
                    "coverRetailerId": False,
                    "customAttributes": None,
                    "customerCaseId": case_id,
                    "customerId": customer['id'],
                    "deviceDetail": "iOS",
                    "imageUrl": "https://d32iiblykc5ytf.cloudfront.net/case/20260126/ef3a4ecd-bdee-4646-b604-40128f6cdace.jpg",
                    "mileage": final_mileage,
                    "operatorId": retailer["id"],
                    "operatorType": "RETAILER",
                    "orderIndex": 3,
                    "os": "ios",
                    "osVersion": "26.2",
                    "programId": 101,
                    "programName": "TCP Program",
                    "programRuleId": 1044,
                    "treadDepth": tread_depth
                },
                {
                    "appVersion": "1.9.14.56",
                    "coverRetailerId": False,
                    "customAttributes": None,
                    "customerCaseId": case_id,
                    "customerId": customer['id'],
                    "deviceDetail": "iOS",
                    "imageUrl": "https://d32iiblykc5ytf.cloudfront.net/case/20260126/473e4c59-4c48-400c-8716-645ac134b7f2.jpg",
                    "mileage": final_mileage,
                    "operatorId": retailer["id"],
                    "operatorType": "RETAILER",
                    "orderIndex": 3,
                    "os": "ios",
                    "osVersion": "26.2",
                    "programId": 101,
                    "programName": "TCP Program",
                    "programRuleId": 1044,
                    "treadDepth": tread_depth
                },
                {
                    "appVersion": "1.9.14.56",
                    "coverRetailerId": False,
                    "customAttributes": None,
                    "customerCaseId": case_id,
                    "customerId": customer['id'],
                    "deviceDetail": "iOS",
                    "imageUrl": "https://d32iiblykc5ytf.cloudfront.net/case/20260126/25dc54a9-6968-4780-90e9-bf7861237d3a.jpg",
                    "mileage": final_mileage,
                    "operatorId": retailer["id"],
                    "operatorType": "RETAILER",
                    "orderIndex": 4,
                    "os": "ios",
                    "osVersion": "26.2",
                    "programId": 101,
                    "programName": "TCP Program",
                    "programRuleId": 1043,
                    "treadDepth": tread_depth
                },
                {
                    "appVersion": "1.9.14.56",
                    "coverRetailerId": False,
                    "customAttributes": None,
                    "customerCaseId": case_id,
                    "customerId": customer['id'],
                    "deviceDetail": "iOS",
                    "imageUrl": "https://d32iiblykc5ytf.cloudfront.net/case/20260126/4a1599b3-d23e-41d4-a1bb-39b11d93b68d.jpg",
                    "mileage": final_mileage,
                    "operatorId": retailer["id"],
                    "operatorType": "RETAILER",
                    "orderIndex": 6,
                    "os": "ios",
                    "osVersion": "26.2",
                    "programId": 101,
                    "programName": "TCP Program",
                    "programRuleId": 15167683,
                    "treadDepth": tread_depth
                }
        ]
        res = self.send_request('post', url, params=params, json=json_data)
        return res
