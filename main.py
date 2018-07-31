from flask import Flask, Blueprint
from flask_restful import Api
from mongoengine import register_connection

from resources.recipes import RecipeAPI
from resources.ingredients import IngredientAPI

from database import db, FLASK_MONGODB_SETTINGS

# create flask app
app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = FLASK_MONGODB_SETTINGS

# connect with database

register_connection('default', **FLASK_MONGODB_SETTINGS)
db.init_app(app)

# register routes

@app.route('/')
def index():
    return 'Hello World', 200

# create blueprints

app_blueprint = Blueprint('api', __name__, url_prefix='/api')

# register resources

api_v1 = Api(app_blueprint, prefix='/v1')
api_v1.add_resource(
    RecipeAPI,
    '/recipe',
    '/recipe/<category>',
    '/recipe/like/<recipe_id>'
)
api_v1.add_resource(IngredientAPI, '/ingredient/<category>')

# register blueprints
app.register_blueprint(app_blueprint)

if __name__ == '__main__':

    app.run(host="0.0.0.0", port='7465', debug=False)
