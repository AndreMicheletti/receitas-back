import os

from flask import Flask, Blueprint
from flask_restful import Api

from resources.recipes import RecipeAPI
from resources.ingredients import IngredientAPI
from resources.categories import CategoryAPI

from mongoengine import connect

# create flask app
app = Flask(__name__)
app_blueprint = Blueprint('api', __name__, url_prefix='/api')

# register APIs
api_v1 = Api(app_blueprint, prefix='/v1')

api_v1.add_resource(RecipeAPI, '/recipe', '/recipe/<recipe_id>')
api_v1.add_resource(IngredientAPI, '/ingredient')
api_v1.add_resource(CategoryAPI, '/category')

# register blueprints
app.register_blueprint(app_blueprint)

if __name__ == '__main__':
    from database import DATABASE_NAME

    connect(db=DATABASE_NAME)
    app.run(host='0.0.0.0', port='5555')
