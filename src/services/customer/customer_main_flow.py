from apis.customer.customer_main_api import CustomerMainApi
from utils.extract import Extract


class CustomerMainFlow:

    def __init__(self):
        self.api = CustomerMainApi()
        self.context = {}
        self._reset_context()
    
    def _reset_context(self):
        """重置上下文"""
        self.context = {
            "customer": None,
            "retailer": None,
            "registration_id": None,
            "item_ids": [],
            "case_ids": []
        }

    def set_customer(self, customer):
        """设置当前操作的客户"""
        self.context['customer'] = customer
    
    def register_case(self, customer, retailer, vehicle, register_data):
        """注册轮胎案例"""
        final_customer = customer or self.context['customer']
        final_retailer = retailer or self.context['retailer']

        # 调用注册接口
        res = self.api.register_api(
            retailer=final_retailer,
            customer=final_customer,
            vehicle=vehicle,
            mileage=register_data['mileage'],
            purchase_photo=register_data['purchase_photo'],
            purchase_date=register_data['purchase_date'],
            tyres=register_data['tyres']
        )
        
        # 提取注册ID和item ID
        if res.get('code') != 0:
            raise ValueError("customer注册请求错误")

        registration_id = Extract.extract_json(res, "data.customerTyreRegistrationId")
        self.context['registration_id'] = registration_id

        # 获取items信息
        vehicle_id = vehicle.get('id')
        if not vehicle_id:
            raise ValueError("没有vehicle id")

        items_res = self.api.registration_items_api(customer=final_customer, vehicle_id=vehicle_id)
        if items_res.get('code') != 0:
            raise ValueError("customer item list请求错误")
        for item in items_res.get('data').get('result'):
            self.context['item_ids'].append(Extract.extract_json(item, "id"))
        
        return res


    def file_case(self, customer, retailer, registration_id, item_ids):
        """提交案例"""
        final_customer = customer or self.context['customer']
        final_retailer = retailer or self.context['retailer']
        registration_id = registration_id or  self.context['registration_id']

        item_ids = item_ids or self.context['item_ids']

        if not registration_id:
            raise ValueError("没有registration_id")

        
        result = []
        
        # 遍历所有注册ID和item ID
        for item_id in item_ids:

            res = self.api.file_api(
                customer=final_customer,
                retailer=final_retailer,
                registration_id=registration_id,
                item_id=item_id
            )
            result.append(res)
            
            # 提取case ID
            if res.get('code') != 0:
                raise ValueError("file case失败")

            case_id = Extract.extract_json(res, "data.id")
            if case_id:
                self.context['case_ids'].append(case_id)
        
        return result
