from mongoengine import connect

from models.recipe import Recipe
from database import FLASK_MONGODB_SETTINGS


know_mistakes = [
    ('ovos', 'ovo'),
    ('pitada sal', 'sal'),
    ('copo leite', 'leite'),
    ('creme leite fresco', 'creme leite'),
    ('creme leite o', 'creme leite'),
    ('gema', 'gemas'),
    ('manteiga sem sal', 'manteiga'),
    ('manteiga amolecida', 'manteiga'), ('manteiga, amolecida', 'manteiga'),
    ('claras ovo', 'claras'),
    ('óleo para fritas', 'óleo'), ('óleo para fritar', 'óleo'),
    ('oleo', 'óleo'),
    ('oleo de cozinha', 'óleo'), ('óleo de cozinha', 'óleo'),
    ('açucar confeiteiro para polvilhar', 'açucar confeiteiro'),
    ('1/2 açucar', 'açucar'),
    ('chocolate meio amargo picado', 'chocolate meio amargo'),
    ('vidro leite coco', 'leite coco')
]


def rename_ingredients(ingredient_tuple_list):

    connect(**FLASK_MONGODB_SETTINGS, alias='default')

    if isinstance(ingredient_tuple_list, tuple):
        ingredient_tuple_list = [ingredient_tuple_list]

    for original_name, new_name in ingredient_tuple_list:
        r = Recipe.objects(ingredients__name=original_name).update(set__ingredients__S__name=new_name.strip())
        print(f"RENAMED {original_name} TO {new_name} :: {r}")

    print("DONE!")


bad_words_list = ['1/2', '3/4', '1/4', ',', '!']


def remove_bad_words():

    connect(**FLASK_MONGODB_SETTINGS, alias='default')

    for recipe in Recipe.objects():
        ings = recipe.ingredients
        new_ingredients = []
        for bad_word in bad_words_list:
            for ing in ings:
                ing.name = ing.name.replace(bad_word, '').strip()
                ing.quantity = str(ing.quantity)
                new_ingredients.append(ing)
        Recipe.objects(id=recipe.id).update_one(ingredients=new_ingredients)
    print("DONE!")


def general_sanity():

    connect(**FLASK_MONGODB_SETTINGS, alias='default')

    print(f"REMOVING BAD WORDS OF {Recipe.objects().count()}")
    remove_bad_words()

    print("DONE!\nRENAMING KNOW MISTAKES IN INGREDIENTS")
    rename_ingredients(know_mistakes)
    print("DONE!")

