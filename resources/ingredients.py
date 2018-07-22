from flask_restful import Resource
from models.recipe import Recipe


class IngredientAPI(Resource):

    def get(self):

        all_ingredients = Recipe._get_collection().aggregate([
            {"$unwind": "$ingredients"},
            {"$group": {
                "_id": "$ingredients.name",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ])

        return {"success": [
            {"name": ing['_id'], "count": ing['count']} for ing in all_ingredients
        ]}, 200

    def post(self):
        pass
