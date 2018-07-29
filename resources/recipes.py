from bson import is_valid as is_valid_objid
from flask import request
from flask_restful import Resource, reqparse

from models.recipe import Recipe


class RecipeAPI(Resource):

    def get(self, category=None, recipe_id=None):

        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, default=20)
        parser.add_argument('page', type=int, default=0)

        args = parser.parse_args()
        limit = args['limit']
        page = args['page']

        skip = (page * limit)
        all_recipes = Recipe.objects().skip(skip).limit(limit)

        return {"success": [rec.to_dict() for rec in all_recipes]}, 200

    def post(self, category=None, recipe_id=None):
        from controllers.recipes import calculate_and_filter_recipe_scores

        args = request.get_json()
        ingredients = args.get('ingredients', None)
        limit = args.get('limit', 3)

        if not ingredients:
            return {"error": "you must provide 'ingredients' argument"}, 500

        recipes = list(Recipe.objects(category=category, ingredients__name__in=ingredients))

        result = calculate_and_filter_recipe_scores(ingredients, recipes)
        return {"success": result[:limit]}, 200

    def put(self, recipe_id=None, **kwargs):

        if not recipe_id:
            return {"error": "must provide category and recipe id within the url"}, 500

        r = Recipe.objects(id=recipe_id).update_one(inc__likes=1)

        if r:
            return {"success": Recipe.objects(id=recipe_id).first().to_dict()}
        return {"error": "unknown"}, 500
