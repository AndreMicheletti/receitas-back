from bson import is_valid as is_valid_objid
from flask import request
from flask_restful import Resource, reqparse

from models.recipe import Recipe


class RecipeAPI(Resource):

    def get(self, recipe_id=None):

        if recipe_id and is_valid_objid(recipe_id):
            recipe = Recipe.objects(id=recipe_id).first()
            return {"success": recipe.to_dict()}, 200

        else:
            parser = reqparse.RequestParser()
            parser.add_argument('limit', type=int, default=10)

            args = parser.parse_args()
            limit = args['limit']

            all_recipes = Recipe.objects().limit(limit)

            return {"success": [rec.to_dict() for rec in all_recipes]}, 200

    def post(self):

        args = request.get_json()
        ingredients = args['ingredients']

        recipes = Recipe.objects(ingredients__name__in=ingredients)

        return {"success": [rec.to_dict() for rec in recipes]}, 200
