from flask_restful import Resource
from models.recipe import Recipe


class CategoryAPI(Resource):

    def get(self):

        all_categories = Recipe._get_collection().aggregate({
            {"$group": {
                "_id": "$category"
            }},
        })

        return {"success": list(all_categories.values())}, 200

    def post(self):
        pass
