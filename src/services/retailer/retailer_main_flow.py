from loguru import logger

from utils.extract import Extract
from src.apis.retailer.retailer_main_api import RetailerMainApi
from tests.data.mock_data import mock_customer_info, mock_vehicle_info


class RetailerMainFlow:

    def __init__(self):
        self.api = RetailerMainApi()
        self.context = {}
        self._reset_context()

    def _reset_context(self):
        """ 每次用例开始前清空 context """
        self.context = {
            'retailer': {},
            'customer': {},
            'vehicle': None,
            'registration_id': None,
            'item_ids': [],
            'case_ids': []
        }

    def set_retailer(self, retailer):
        """设置当前操作的零售商"""
        self.context['retailer'] = retailer

    def register_case(self, retailer, customer, vehicle, register_data):
        final_retailer = retailer or self.context['retailer']
        final_customer = customer
        final_vehicle = vehicle

        self.context['customer'] = final_customer
        self.context['vehicle'] = final_vehicle

        if not final_retailer:
            raise ValueError("零售商信息不能为空")

        # 构建调用参数
        res = self.api.register_api(
            retailer=final_retailer,
            customer=final_customer,
            vehicle=final_vehicle,
            mileage=register_data.get('mileage'),
            purchase_photo=register_data.get('purchase_photo'),
            purchase_date=register_data.get('purchase_date'),
            tyres=register_data.get('tyres')
        )

        # 提取数据到context
        registration_id = Extract.extract_json(res, "data.customerTyreRegistrationId")
        vehicle_id = Extract.extract_json(res, "data.customerVehicleId")
        customer_id = Extract.extract_json(res, "data.customerId")
        if not customer_id or not registration_id or not vehicle_id:
            logger.error(
                f"注册返回数据不齐: registration_id={registration_id}, "
                f"vehicle_id={vehicle_id}, customer_id={customer_id}, res={res}"
            )
            raise ValueError(
                f"以下数据不齐，registration_id={registration_id} "
                f"vehicle_id={vehicle_id} customer_id={customer_id}"
            )

        self.context['customer']['id'] = customer_id
        self.context['vehicle']['id'] = vehicle_id
        self.context['registration_id'] = registration_id

        return res

    def registration_items_case(self, retailer, vehicle_id):
        final_retailer = retailer or self.context['retailer']
        vehicle_id = vehicle_id or self.context['vehicle'].get('id')

        if not final_retailer:
            raise ValueError("零售商信息不能为空")

        if not vehicle_id:
            raise ValueError("车辆ID不能为空")

        status = 1
        res = self.api.registration_items_api(
            retailer=final_retailer,
            vehicle_id=vehicle_id,
            status=status
        )

        for item in res.get("data").get('result'):
            item_id = Extract.extract_json(item, "id")
            self.context['item_ids'].append(item_id)

        return res


    def file_case(self, retailer, customer, registration_id, item_ids):
        final_retailer = retailer or self.context['retailer']
        final_customer = customer or self.context['customer']

        registration_id = registration_id or self.context['registration_id']
        items_id = item_ids or self.context['item_ids']

        if not final_retailer:
            raise ValueError("零售商信息不能为空")

        ress = []

        for item_id in items_id:
            res = self.api.file_api(
                retailer=final_retailer,
                customer=final_customer,
                registration_id=registration_id,
                item_id=item_id
            )
            ress.append(res)
            case_id = Extract.extract_json(res, "data.id")
            self.context['case_ids'].append(case_id)

        return ress


    def validate_case(self, retailer, customer, case_ids, validate_data):
        final_retailer = retailer or self.context['retailer']
        final_customer = customer or self.context['customer']
        case_ids = case_ids or self.context['case_ids']

        if not final_retailer:
            raise ValueError("零售商信息不能为空")

        ress = []
        for case_id in case_ids:
            res = self.api.validate_api(
                retailer=final_retailer,
                customer=final_customer,
                case_id=case_id,
                **validate_data
            )
            ress.append(res)

        return ress
