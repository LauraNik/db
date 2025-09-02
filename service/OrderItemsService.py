from model.OrderItemsModel import OrderItemsModel
from service.BaseService import BaseService

class OrderItemsService(BaseService):
    def __init__(self):
        super().__init__(OrderItemsModel)
