from flask_restful import reqparse
from flask import request

from utils.database_connection import DatabaseConnection
from endpoints.base_resource import AuthenticatedResource


class CategoriesResource(AuthenticatedResource):
    """
    Recurso para gestionar categorías.
    Hereda de AuthenticatedResource para reutilizar la validación de token.
    """

    def __init__(self):
        # Ajusta el nombre del archivo JSON según tu estructura real
        self.db = DatabaseConnection("categories.json")
        self.db.connect()
        self.categories_data = self.db.get_categories()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name",
            type=str,
            required=True,
            help="Name of the category"
        )

    def get(self, category_id=None):
        # 1. Validar token con la clase base
        error = self._require_valid_token()
        if error:
            return error

        # 2. Lógica de consulta
        if category_id is not None:
            category = next(
                (c for c in self.categories_data if c["id"] == category_id),
                None,
            )
            if category is not None:
                return category, 200
            else:
                return {"message": "Category not found"}, 404

        # Sin id -> devolver todas
        return self.categories_data, 200

    def post(self):
        # 1. Validar token con la clase base
        error = self._require_valid_token()
        if error:
            return error

        # 2. Crear nueva categoría
        args = self.parser.parse_args()
        category_name = args["name"]

        new_category = {
            "id": len(self.categories_data) + 1,
            "name": category_name,
        }

        self.categories_data.append(new_category)
        self.db.add_category(new_category)

        return {
            "message": "Category added successfully",
            "category": new_category,
        }, 201

    def delete(self):
        # 1. Validar token con la clase base
        error = self._require_valid_token()
        if error:
            return error

        # 2. Borrar categoría por nombre
        args = self.parser.parse_args()
        category_name = args["name"]

        if not category_name:
            return {"message": "Category name is required"}, 400

        category_to_remove = next(
            (cat for cat in self.categories_data if cat["name"] == category_name),
            None,
        )

        if category_to_remove is None:
            return {"message": "Category not found"}, 404

        # Filtrar lista en memoria
        self.categories_data = [
            cat for cat in self.categories_data if cat["name"] != category_name
        ]

        # Actualizar en la "BD"
        self.db.remove_category(category_name)

        return {"message": "Category removed successfully"}, 200
