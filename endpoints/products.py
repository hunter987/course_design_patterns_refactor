from flask_restful import reqparse
from flask import request
from utils.database_connection import DatabaseConnection
from endpoints.base_resource import AuthenticatedResource


class ProductsResource(AuthenticatedResource):
    def __init__(self):
        self.db = DatabaseConnection('db.json')
        self.db.connect()

        self.products = self.db.get_products()
        self.parser = reqparse.RequestParser()

    def get(self, product_id=None):
        # 1. Validar token usando la clase base
        error = self._require_valid_token()
        if error:
            return error

        # 2. Lógica original
        args = self.parser.parse_args()  # se mantiene aunque no tenga argumentos definidos
        category_filter = request.args.get('category')

        if category_filter:
            filtered_products = [
                p for p in self.products
                if p['category'].lower() == category_filter.lower()
            ]
            return filtered_products

        if product_id is not None:
            product = next((p for p in self.products if p['id'] == product_id), None)
            if product is not None:
                return product
            else:
                return {'message': 'Product not found'}, 404

        return self.products

    def post(self):
        # 1. Validar token usando la clase base
        error = self._require_valid_token()
        if error:
            return error

        # 2. Lógica original para crear producto
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the product')
        parser.add_argument('category', type=str, required=True, help='Category of the product')
        parser.add_argument('price', type=float, required=True, help='Price of the product')

        args = parser.parse_args()

        new_product = {
            'id': len(self.products) + 1,
            'name': args['name'],
            'category': args['category'],
            'price': args['price']
        }

        self.products.append(new_product)
        self.db.add_product(new_product)

        return {'mensaje': 'Product added', 'product': new_product}, 201