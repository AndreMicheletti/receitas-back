from flask_mongoengine import MongoEngine

# MONGO_CONN_STRING = "mongodb://recipes:CymGZDAHp2fCpbQp@asynccluster-fue3b.gcp.mongodb.net/recipes"

db = MongoEngine()

FLASK_MONGODB_SETTINGS = {
    'db': 'recipes',
    'host': "mongodb+srv://master:fqa5HXjpNRr51z75@cluster0-fue3b.mongodb.net/recipes"
}
