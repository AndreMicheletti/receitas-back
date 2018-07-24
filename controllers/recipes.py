from typing import List
from models.recipe import Recipe


def calculate_and_filter_recipe_scores(
        user_ingredients: List[str],
        fetched_recipes: List[Recipe]
    ) -> List[dict]:

    result = []

    for recipe in fetched_recipes:

        this_recipe_score = 0
        this_recipe_ingredients = [ing.name for ing in recipe.ingredients]

        # score :: has all ingredients
        if all([ing in this_recipe_ingredients for ing in user_ingredients]):
            this_recipe_score += 50

        # score :: has few ingredients
        this_recipe_score -= len(this_recipe_ingredients)

        result.append({
            **recipe.to_dict(),
            'score': this_recipe_score
        })

    return sorted(result, key=lambda x: x['score'], reverse=True)
