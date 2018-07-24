from flask import Flask, Blueprint
from flask_restful import Api
from mongoengine import register_connection

from resources.recipes import RecipeAPI
from resources.ingredients import IngredientAPI

from database import db, FLASK_MONGODB_SETTINGS

# create flask app
app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = FLASK_MONGODB_SETTINGS

app_blueprint = Blueprint('api', __name__, url_prefix='/api')

# CONNECT WITH DATABASE

register_connection('default', **FLASK_MONGODB_SETTINGS)
db.init_app(app)

# register APIs
api_v1 = Api(app_blueprint, prefix='/v1')

api_v1.add_resource(RecipeAPI, '/recipe', '/recipe/<category>')
api_v1.add_resource(IngredientAPI, '/ingredient/<category>')

# register blueprints
app.register_blueprint(app_blueprint)

if __name__ == '__main__':

    app.run(host="0.0.0.0", port='7465', debug=False)
