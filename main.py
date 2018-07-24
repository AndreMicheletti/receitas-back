import os

from flask import Flask, Blueprint
from flask_restful import Api

from resources.recipes import RecipeAPI
from resources.ingredients import IngredientAPI

from mongoengine import connect

# create flask app
app = Flask(__name__)
app_blueprint = Blueprint('api', __name__, url_prefix='/api')

# register APIs
api_v1 = Api(app_blueprint, prefix='/v1')

api_v1.add_resource(RecipeAPI, '/recipe', '/recipe/<category>')
api_v1.add_resource(IngredientAPI, '/ingredient/<category>')

# register blueprints
app.register_blueprint(app_blueprint)

if __name__ == '__main__':
    from database import DATABASE_NAME, MONGO_CONN_STRING_MASTER

    is_prod = os.getenv("ENV_MODE", "local") == "PROD"
    if is_prod:
        connect(db=DATABASE_NAME, host=MONGO_CONN_STRING_MASTER)
    else:
        connect(db=DATABASE_NAME)

    app.run(host="0.0.0.0", port='7465', debug=not is_prod)
