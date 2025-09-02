from service.ProductsService import ProductsService

class ProductsView(object):
    def __init__(self):
        self.service = ProductsService()

    def add_product(self, data):
        # TODO remove return
        return self.service.create_entity(data)

    def update_stock(self, *args):
        return self.service.update_entity(*args)
    
    def delete_product(self, data):
        return self.service.delete_entity(data)
    
    def list_products(self):
        status, rows = self.service.get_entities()
        # TODO
        if not status:
            return status
        for row in rows:
            print(row)

        return status