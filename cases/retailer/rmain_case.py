from loguru import logger

from apis.retailer.rmain_api import RMainApi


class RMainCase(RMainApi):

    def __init__(self):
        super().__init__()
        self.context = {}
        self._reset_context()

    def _reset_context(self):
        """ 每次用例开始前清空 context """
        self.context = {
            'customer': {'phone': None, 'name': None, 'id': None},
            'vehicle': {'plate_number': None, 'id': None},
            'registration_id': None,
            'items_id': [],
            'cases_id': []
        }


    def register_case(self, register_data, db):
        self._reset_context()
        final = register_data.copy()

        customer = self._build_customer_info(register_data, db)
        vehicle = self._build_vehicle_info(register_data, db)

        final.pop('customer_phone', None)
        final.pop('customer_name', None)
        final.pop('plate_number', None)
        final.update({'customer': customer})
        final.update({'vehicle': vehicle})

        res = self.register_api(**final)

        # 提取数据到context
        extract_info = self.extract_info_from_response(response=res,
                                                       keys_path={"registration_id": ["data", "customerTyreRegistrationId"],
                                                                  "vehicle_id": ["data", "customerVehicleId"],
                                                                  "customer_id": ["data", "customerId"]})

        self.context['customer']['id'] = extract_info['customer_id']
        self.context['vehicle']['id'] = extract_info['vehicle_id']
        self.context['registration_id'] = extract_info['registration_id']
        logger.debug(f"registration_id: {self.context['registration_id']}")
        logger.debug(f"vehicle: {self.context['vehicle']}")
        logger.debug(f"customer: {self.context['customer']}")

        self.registration_items_case()

        return res

    def registration_items_case(self):
        vehicle_id = self.context['vehicle']['id']
        registration_id = self.context['registration_id']
        status = 1
        res = self.registration_items_api(vehicle_id=vehicle_id, status=status)
        self.extract_info_from_response(response=res, keys_path={})
        items_id = [item['id'] for item in res.get('data', {}).get('result', [])
                    if item.get('customerTyreRegistrationId') == registration_id]
        self.context['items_id'] = items_id
        logger.debug(f"items_id: {self.context['items_id']}")
        return res


    def file_case(self):
        registration_id = self.context['registration_id']
        items_id = self.context['items_id']
        customer = self.context['customer']
        ress = []
        cases_id = []
        for item_id in items_id:
            res = self.file_api(registration_id=registration_id, item_id=item_id, customer=customer)
            ress.append(res)
            extract_info = self.extract_info_from_response(response=res, keys_path={"case_id": ["data", "id"]})
            cases_id.append(extract_info['case_id'])
        self.context['cases_id'] = cases_id
        logger.debug(f"cases_id: {self.context['cases_id']}")
        return ress


    def validate_case(self, validate_data):
        cases_id = self.context['cases_id']
        ress = []
        for case_id in cases_id:
            res = self.validate_api(case_id=case_id, customer=self.context['customer'], **validate_data)
            ress.append(res)
        return ress


    def _build_customer_info(self, register_data, db):
        phone = register_data.get('customer_phone', None)
        name = register_data.get('customer_name', None)
        self.context['customer'].update({'phone': phone, 'name': name, 'id': None})
        if phone:
            info = db.query_one("select * from customers where account_id = 3 and phone = %s;",
                                phone)
            if info:
                self.context['customer']['id'] = info['id']
            else:
                logger.info(f"在数据库中未找到手机号为 {phone} 的客户信息")
        return self.context['customer']


    def _build_vehicle_info(self, register_data, db):
        plate_number = register_data.get('plate_number', None)
        self.context['vehicle'].update({'plate_number': plate_number, 'id': None})
        if plate_number:
            info = db.query_one("select * from customer_vehicles where account_id = 3 and plate_number = %s;", plate_number)
            if info:
                self.context['vehicle']['id'] = info['id']
            else:
                logger.info(f"在数据库中未找到车牌号为 {plate_number} 的车辆信息")
        return self.context['vehicle']


    # def _merge_step_1_and_2(self, register_data, db):
    #     # 注册轮胎，获取 注册id
    #     register_res = self.register_case(register_data, db)
    #     register_extract = self.extract_info_from_response(response=register_res,
    #                                                        keys_path={
    #                                                            "registration_id": ["data", "customerTyreRegistrationId"],
    #                                                            "vehicle_id": ["data", "customerVehicleId"],
    #                                                            "customer_id": ["data", "customerId"],
    #                                                        })
    #     registration_id = register_extract['registration_id']
    #     vehicle_id = register_extract['vehicle_id']
    #     customer_id = register_extract['customer_id']
    #     # 防止之前build vehicle和customer信息时
    #     self.context.update({'registration_id': registration_id})
    #     self.context['vehicle'].update({'id': vehicle_id})
    #     self.context['customer'].update({'id': customer_id})
    #
    #     # 查询注册的全部items id
    #     logger.debug(f"之前self.context: {self.context}")
    #     items_list_res = self.registration_items_api(vehicle_id=vehicle_id, status=1)
    #     self.extract_info_from_response(items_list_res, {})
    #     items_id = [item['id'] for item in items_list_res.get('data', {}).get('result', [])
    #                 if item.get('customerTyreRegistrationId') == registration_id]
    #     self.context.update({'items_id': items_id})
    #     logger.debug(f"之后self.context: {self.context}")

