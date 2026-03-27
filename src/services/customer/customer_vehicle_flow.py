from apis.customer.customer_vehicle_api import CustomerVehicleApi
from utils.extract import Extract


class CustomerVehicleFlow:
    def __init__(self):
        self.vehicle_api = CustomerVehicleApi()
        self.context = {}
        self._reset_context()

    def _reset_context(self):
        self.context = {
            'customer': None,
            "vehicle_id": None
        }
    
    def set_customer(self, customer):
        """设置当前操作的用户"""
        self.context['customer'] = customer

    def add_vehicle_case(self, customer, vehicle_data):
        final_customer = customer or self.context["customer"]
        res = self.vehicle_api.add_vehicle_api(customer=final_customer, vehicle=vehicle_data)
        # 提取数据vehicle_id
        vehicle_id = Extract.extract_json(res, "data.id")
        # 存入context
        self.context["vehicle_id"] = vehicle_id
        return res

    def update_vehicle_case(self, customer, vehicle_id, vehicle_data):
        final_customer = customer or self.context["customer"]
        final_vehicle_id = vehicle_id or self.context["vehicle_id"]
        if not final_vehicle_id:
            raise ValueError("update_vehicle_case缺少vehicle_id")
        res = self.vehicle_api.update_vehicle_api(vehicle_id=final_vehicle_id, customer=final_customer, vehicle=vehicle_data)
        return res

    def delete_vehicle_case(self, customer, vehicle_id):
        final_customer = customer or self.context["customer"]
        final_vehicle_id = vehicle_id or self.context["vehicle_id"]
        if not final_vehicle_id:
            raise ValueError("delete_vehicle_case缺少vehicle_id")
        res = self.vehicle_api.delete_vehicle_api(
            customer=final_customer,
            vehicle_id=final_vehicle_id,
        )
        return res

    def list_vehicle_case(self, customer):
        final_customer = customer or self.context["customer"]
        res = self.vehicle_api.list_vehicle_api(customer=final_customer)
        return res

