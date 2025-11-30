from flask_restful import reqparse
from flask import request
from utils.database_connection import DatabaseConnection
from endpoints.base_resource import AuthenticatedResource


class FavoritesResource(AuthenticatedResource):
    def __init__(self):
        self.db = DatabaseConnection('favorites.json')
        self.db.connect()
        self.favorites = self.db.get_favorites()
        self.parser = reqparse.RequestParser()

    def get(self, favorite_id=None):
        # 1. Validar token con la clase base
        error = self._require_valid_token()
        if error:
            return error

        # 2. Lógica original
        if favorite_id is not None:
            favorite = next(
                (f for f in self.favorites if f['id'] == favorite_id),
                None
            )
            if favorite is not None:
                return favorite
            else:
                return {'message': 'Favorite not found'}, 404

        return self.favorites

    def post(self):
        # 1. Validar token con la clase base
        error = self._require_valid_token()
        if error:
            return error

        # 2. Parsear argumentos (ajusta si tu versión original difiere)
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', type=int, required=True, help='ID of the product')
        parser.add_argument('user_id', type=int, required=True, help='ID of the user')

        args = parser.parse_args()

        new_favorite = {
            'id': len(self.favorites) + 1,
            'product_id': args['product_id'],
            'user_id': args['user_id']
        }

        self.favorites.append(new_favorite)
        self.db.add_favorite(new_favorite)

        return {'message': 'Favorite added', 'favorite': new_favorite}, 201

    def delete(self):
        token = request.headers.get('Authorization')
        if not token:
            return { 'message': 'Unauthorized acces token not found'}, 401
        if not is_valid_token(token):
           return { 'message': 'Unauthorized invalid token'}, 401

        args = self.parser.parse_args()
        self.parser.add_argument('name', type=str, required=True, help='Name of the category')
        args = self.parser.parse_args()
        category_name = args['name']
 
        if not category_name:
            return {'message': 'Category name is required'}, 400

        category_to_remove = next((cat for cat in self.categories_data if cat["name"] == category_name), None)

        if category_to_remove is None:
            return {'message': 'Category not found'}, 404
        else:
            categories = [cat for cat in self.categories_data if cat["name"] != category_to_remove]
            self.categories_data = categories
            self.db.remove_category(category_name)

            return {'message': 'Category removed successfully'}, 200

