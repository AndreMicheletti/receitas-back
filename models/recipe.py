import json

from mongoengine import *


measures_types = {
    # GRAMAS
    'g': ['g', 'g.', 'gs', 'gramas', 'grama'],

    # UNIDADES
    'un': ['unidades', 'un', 'un.', 'embalagem', 'caixa', 'caixas', 'embalagens'],

    # LITROS
    'l': ['l', 'l.', 'lt', 'lt.', 'lts', 'lts.', 'litros', 'litro'],

    # MLS
    'ml': ['ml', 'ml.', 'mls', 'mls.'],

    # XÍCARA
    'xiraca': ['xícara', 'xícaras', 'xicara', 'xicaras'],

    # LATAS
    'lata': ['lata', 'latas'],

    # COLHER
    'colher': ['colher', 'colheres']
}

remove_words = ['de', 'gosto', 'cheia', 'cheio']


def is_number(x):
    try:
        if '/' in x:
            v1, v2 = x.split('/')
            v1 = float(v1)
            v2 = float(v2)
            return x
        return float(x)
    except ValueError:
        return False


class EmbeddedIngredient(EmbeddedDocument):

    name = StringField()
    quantity = StringField()
    measure = StringField()


class Recipe(Document):

    name = StringField(required=True)
    url = URLField(required=True, unique=True)
    category = StringField(required=True)

    photo = StringField(default="")

    ingredients = ListField(EmbeddedDocumentField(EmbeddedIngredient))
    ingredients_pretty = ListField(StringField())

    instructions = ListField(StringField())

    portion_yield = IntField()

    likes = IntField(default=0)

    meta = {
        'indexes': [
            'category', 'photo', 'ingredients',
            ('category', 'ingredients')
        ],
        'db-alias': 'default'
    }

    def __repr__(self):
        return f'<Recipe {str(self.id)} - {self.name}>'

    def to_dict(self) -> dict:
        result = json.loads(self.to_json())
        result.pop('_id')
        return {
            'id': str(self.id),
            **result
        }

    def parse_and_save_ingredient_strings(self, ingredients_list):
        self.ingredients = [Recipe.parse_ingredient(ing) for ing in ingredients_list]

    @staticmethod
    def parse_ingredient(ingredient_str) -> EmbeddedIngredient:

        ingredient_str = ingredient_str.replace('a gosto', '')

        words = [w.strip().lower() for w in ingredient_str.split(' ') if w not in remove_words]
        words = [w for w in words if '(' not in w and ')' not in w]
        selected_measure_type = 'un'

        for measure_type, measure_words in measures_types.items():
            if any([m in words for m in measure_words]):
                selected_measure_type = measure_type
                [words.remove(w) for w in measures_types[selected_measure_type] if w in words]

        quantity = 1
        for word in words:
            n = is_number(word)
            if n is not False:
                quantity = n
                words.remove(word)
                break

        result = EmbeddedIngredient()
        result.name = " ".join(words)
        result.quantity = quantity
        result.measure = selected_measure_type
        return result
