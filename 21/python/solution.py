import os
import time
from dataclasses import dataclass
from typing import List

infile = "input"
path = os.path.dirname(os.path.realpath(__file__))


@dataclass
class Food:
    ingredients: List[str]
    allergens: List[str]


def parse_line(line, foods):
    allergies = False
    ingredients = []
    allergens = []
    for tok in line.split():
        if not allergies:
            if "contains" in tok:
                allergies = True
                continue
            ingredients.append(tok)
        else:
            allergens.append(tok[:-1])
    foods.append(
        Food(ingredients=ingredients,
             allergens=allergens)
    )


def no_allergens(foods):
    d = dict()
    for food in foods:
        for allergen in food.allergens:
            if allergen not in d:
                d[allergen] = set(food.ingredients)
            else:
                d[allergen] = d[allergen].intersection(food.ingredients)
    safe = list()
    unsafe = set()
    for ingredients in d.values():
        for ingredient in ingredients:
            unsafe.add(ingredient)
    for food in foods:
        for ingredient in food.ingredients:
            if ingredient not in unsafe:
                safe.append(ingredient)
    num_safe = len(safe)
    allergens = list(map(lambda item: (len(item[1]), item[0], item[1]), d.items()))
    allergens.sort(reverse=True)
    canonical = []
    while len(allergens) > 0:
        _, allergen, ingredients = allergens.pop()
        ingredient = ingredients.pop()
        canonical.append((allergen, ingredient))
        allergens_prime = []
        while len(allergens) > 0:
            n, a, s = allergens.pop()
            if ingredient in s:
                s.remove(ingredient)
            allergens_prime.append((len(s), a, s))
        allergens = allergens_prime
        allergens.sort(reverse=True)
    canonical.sort()
    result = map(lambda tup: tup[1], canonical)
    result_str = ",".join(result)
    return num_safe, result_str


def main(infile=infile):
    input_file = f"{path}/resources/{infile}"
    foods = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            parse_line(line, foods)
    start = time.monotonic()
    result = no_allergens(foods)
    end = time.monotonic()
    return result[0], result[1], end - start


def display(num_safe: int, allergens: str, elapsed_time):
    print(f"num_safe: {num_safe}")
    print(f"allergens: {allergens}")
    print(f"elapsed time: {elapsed_time}")


if __name__ == '__main__':
    num_safe, allergens, elapsed_time = main()
    display(num_safe, allergens, elapsed_time)
