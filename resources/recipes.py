from bson import is_valid as is_valid_objid
from flask import request
from flask_restful import Resource, reqparse

from models.recipe import Recipe


class RecipeAPI(Resource):

    def get(self, category=None):

        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, default=20)
        parser.add_argument('page', type=int, default=0)

        args = parser.parse_args()
        limit = args['limit']
        page = args['page']

        skip = (page * limit)
        all_recipes = Recipe.objects().skip(skip).limit(limit)

        return {"success": [rec.to_dict() for rec in all_recipes]}, 200

    def post(self, category=None):

        args = request.get_json()
        ingredients = args.get('ingredients', None)
        limit = args.get('limit', 3)

        if not ingredients:
            return {"error": "you must provide 'ingredients' argument"}, 500

        recipes = list(Recipe.objects(category=category, ingredients__name__in=ingredients))

        result = []
        for recipe in recipes:
            ingredient_names = [ing.name for ing in recipe.ingredients]
            count = 0
            for _ in [ing for ing in ingredients if ing in ingredient_names]:
                count += 1
            rating = len(ingredient_names) - count
            if count == len(ingredients):
                rating -= 100
            result.append({
                **recipe.to_dict(),
                'rating': rating
            })
        result = sorted(result, key=lambda x: x['rating'])

        return {"success": result[:limit]}, 200
