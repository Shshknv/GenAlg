from numpy import genfromtxt
from random import uniform, randint
import json


def get_data():
    with open('11.txt') as dataSource:
       maxWeight, maxVolume = [float(i) for i in next(dataSource).split()]
       data = genfromtxt('11.txt', delimiter=' ', dtype=(int, float, int), skip_header=1)
    return {
        'maxWeight': int(maxWeight),
        'maxVolume': float(maxVolume),
        'items': data.tolist()
}


def fitness(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > genData['maxWeight'] or volume > genData['maxVolume']:
        price = 0
    return price


# Начальная популяция
def first_population():
    first_set = []
    for i in range(200):
        item = randint(0, 59)
        weight = 0
        list = []
        for j in range(60):
            list.append(0)
        while (weight + genData['items'][item][0]) < genData['maxWeight']:
            list[item] = 1
            weight += genData['items'][item][0]
            if item < len(genData['items']) - 1:
                item += 1
            else:
                item = 0
        first_set.append(list)
    return first_set


# Отбор особей для скрещивания
def sets_filter(sets):
    final_sets = []
    checking_percent = uniform(0, 1)
    fitness_for_sets = []
    for j in range(len(sets)):
        fitness_for_sets.append(fitness(sets[j], genData['items']))
    max_fitness = max(fitness_for_sets)
    for i in range(len(fitness_for_sets)):
        if (max_fitness != 0):
            fitness_for_sets[i] = fitness_for_sets[i] / max_fitness
            if checking_percent < fitness_for_sets[i]:
                final_sets.append(sets[i])
    return final_sets


# Скрещивание
def crossingover(first_parent, second_parent):
    first_child = []
    second_child = []
    for i in range(60):
        x = randint(1, 2)
        if(x == 1):
            first_child.append(first_parent[i])
        else:
            first_child.append(second_parent[i])
    for i in range(60):
        x = randint(1, 2)
        if (x == 1):
            second_child.append(first_parent[i])
        else:
            second_child.append(second_parent[i])
    return [first_child, second_child]


def sets_crossingover(sets):
    child_sets = []
    for i in range(0, len(sets) // 2):
        child_sets += crossingover(sets[i], sets[len(sets) - 1 - i])
    return child_sets


# Мутация
def mutation(sets):
    final_len = round(len(sets) * 0.05)
    changing_sets = sets[:final_len]
    static_sets = sets[final_len:]
    for i in range(len(changing_sets)):
        for j in range(0, 3):
            item = randint(0, len(changing_sets[i]) - 1)
            changing_sets[i][item] = 1 if changing_sets[i][item] == 0 else 0
    return changing_sets + static_sets


def get_max_fitness_for_sets(sets):
    fitness_for_sets = []
    for j in range(len(sets)):
        fitness_for_sets.append(fitness(sets[j], genData['items']))
    return max(fitness_for_sets)


def init():
    current_sets = first_population()
    max_fitness = get_max_fitness_for_sets(current_sets)
    current_count = 0
    for i in range(500):
        filters_sets = sets_filter(current_sets)
        children = sets_crossingover(filters_sets)
        final_children = mutation(children)
        current_sets = final_children  # Новая популяция
        prev_max_fitness = max_fitness
        max_fitness = get_max_fitness_for_sets(current_sets)
        current_percent = abs((max_fitness - prev_max_fitness) / ((max_fitness + prev_max_fitness) / 2)) * 100
        if current_percent == 0:
            current_count += 1
        if current_count > 10:
            break
    result_weight = 0
    result_volume = 0
    result_price = 0
    result_sum = []
    result_set = []
    for i in range(len(current_sets)):
        fitness_for_set = fitness(current_sets[i], genData['items'])
        if fitness_for_set == max_fitness:
            result_set = current_sets[i]
    for i in range(len(result_set)):
        if result_set[i] > 0:
            result_weight += genData['items'][i][0]
            result_volume += genData['items'][i][1]
            result_price += genData['items'][i][2]
            result_sum.append(i)
    res = {
        'weight': result_weight,
        'volume': result_volume,
        'price': result_price,
        'items': result_sum
    }
    with open('result_2.json', 'w') as file:
        json.dump(res, file)


if __name__ == "__main__":
    genData = get_data()
    init()