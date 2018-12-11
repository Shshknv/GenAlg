import json
from pyeasyga import pyeasyga

resultVolume = 0
resultWeight = 0
items = []

with open('11.txt') as dataSource:
    maxWeight, maxVolume = [float(i) for i in next(dataSource).split()]
    data = []
    for line in dataSource:
        data.append([float(i) for i in line.split()])

def fitness(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > maxWeight or volume > maxVolume:
        price = 0
    return price

ga = pyeasyga.GeneticAlgorithm(data)
ga.population_size = 200
ga.fitness_function = fitness
ga.run()

result = ga.best_individual()

for i in range(len(result[1])):
    if result[1][i] == 1:
        items.append(i+1)

for i in range(len(items)):
    resultVolume += data[items[i]-1][1]
    resultWeight += data[items[i]-1][0]

jsonResult = dict(value=result[0], weight=resultWeight, volume=resultVolume, items=items)

with open('result_1.json', 'w') as outfile:
        json.dump(jsonResult, outfile, indent = 4)