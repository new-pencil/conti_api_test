from utils.request import Request


class CustomerVehicleApi(Request):
    """customer vehicle management apis"""

    def add_vehicle_api(self, customer, vehicle):
        """ add vehicle api"""
        url = "/account/3/customer/add/vehicle"
        json_data = {
            "customerId": customer.get('id'),
            "imageUrl": "",
            "manufacturerId": vehicle.get('manufacturer_id'),
            "modelId": vehicle.get('model_id'),
            "plateNumber": vehicle.get('plate_number'),
            "modelName": vehicle.get('model_name'),
            "manufacturerName": vehicle.get('manufacturer_name'),
            "companyCar": vehicle.get('company_car')
        }
        res = self.send_request('post', url, json=json_data)
        return res

    def update_vehicle_api(self, vehicle_id, customer, vehicle):
        """ update vehicle api"""
        url = f"/account/3/customer/update/vehicle/{vehicle_id}"
        json_data = {
            "customerId": customer.get('id'),
            "imageUrl": "",
            "manufacturerId": vehicle.get('manufacturer_id'),
            "modelId": vehicle.get('model_id'),
            "plateNumber": vehicle.get('plate_number'),
            "modelName": vehicle.get('model_name'),
            "manufacturerName": vehicle.get('manufacturer_name'),
            "companyCar": vehicle.get('company_car')
        }
        res = self.send_request('post', url, json=json_data)
        return res

    def delete_vehicle_api(self, customer, vehicle_id):
        """ delete vehicle api"""
        url = f"/account/3/customer/{customer['id']}/delete/vehicle/{vehicle_id}"
        res = self.send_request('get', url)
        return res

    def list_vehicle_api(self, customer):
        """ list vehicle api"""
        url = f"/account/3/customer/{customer['id']}/vehicles"
        res = self.send_request('get', url)
        return res
