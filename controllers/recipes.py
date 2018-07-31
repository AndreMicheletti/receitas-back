from typing import List
from models.recipe import Recipe

from unidecode import unidecode


def calculate_and_filter_recipe_scores(
        user_ingredients: List[str],
        fetched_recipes: List[Recipe]
    ) -> List[dict]:

    result = []

    for recipe in fetched_recipes:

        this_recipe_score = 0
        this_recipe_ingredients = [unidecode(ing.name) for ing in recipe.ingredients]

        # score :: has all ingredients
        if all([ing in this_recipe_ingredients for ing in user_ingredients]):
            this_recipe_score += 250

        # score :: has few ingredients
        this_recipe_score -= (2 * len(this_recipe_ingredients))

        # score :: likes
        this_recipe_score += recipe.likes if recipe.likes else 0

        result.append({
            **recipe.to_dict(),
            'score': this_recipe_score
        })

    return sorted(result, key=lambda x: x['score'], reverse=True)
