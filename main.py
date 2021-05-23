import random
import numpy as np
from graph import plotte_generationen
from graph import plotte_optimum

population_size = 50  # Anzahl der Individuen in der Population (muss für Crossover eine gerade Zahl sein)
generationen = 200  # Anzahl der Generationen
p_m = (1 / 100)  # Mutationswahrscheinlichkeit
p_c = 0.7  # Crossover-Wahrscheinlichkeit


def f(x):
    '''Return des y-Wertes der Funktion, dessen Optimum gefunden werden soll'''
    return 0.0054 * np.power(x, 3) - 0.23 * np.power(x, 2) + 2.5 * x


def genetischer_algorithmus(plotting=False):
    '''
    Aufruf der Methoden für die 5 Schritte eines GA und graphsiche Darstellung der Generationen.
    :param plotting: True, wenn Plots erstellt werden sollen
    :return: int numpy array der Individuen (x-Koordinaten) der letzte Generation
    '''
    population = initialisiere_population()
    if plotting:
        plotte_generationen(population, f"Generation 0")  # plotte die Anfangspopulation
    eliten = []
    for i, generation in enumerate(range(0, generationen)):
        fitness = berechne_fitness(population)
        elite, population = roulette_selektion(population, fitness)  # Alternativ turnier_selektion(population, fitness)
        population = rekombination(population)[:-1]  # ein Individuum wird später durch die Elite ersetzt
        population = mutation(population)
        population = np.hstack((elite, population))  # Die Elite bleibt unverändert erhalten (starker Elitismus)
        eliten.append(elite)  # Eliten speichern für plotte_optimum() Funktion
        if plotting and (i+1) % 100 == 0:  # plotte nur jede 100. Generation
            plotte_generationen(population, f"Generation {i+1}")
    if plotting:
        plotte_optimum(eliten)
    return np.array([dekodieren(i) for i in population])


def initialisiere_population():
    '''
    Return der zufälligen Anfangspopulation
    :return: numpy array der x-Koordinaten jedes Individuums kodiert mit Gray-Code
    '''
    population = [kodieren(random.randint(0, 31000)) for _ in range(population_size)]
    return np.array(population)


def berechne_fitness(population):
    '''
    return der Fitness der Individuen einer Population
    :param population: String numpy array bestehend aus Individuen (x-Koordinaten) kodiert mit Gray-Code
    :return: numpy array der Fitness jedes Individuums
    '''
    x = np.array([dekodieren(individuum) for individuum in population])
    fitness = f(x)
    return np.array(fitness)


def turnier_selektion(population, fitness):
    '''
    Erstellung einer neuen Population durch Auswahl der Individuen mit Turnierselektion
    :param population: String numpy array bestehend aus Individuen (x-Koordinaten) kodiert mit Gray-Code
    :param fitness: numpy array der Fitness jedes Individuums
    :return: Individuum mit höchster Fitness (String) und String numpy array der neuen population kodiert mit Gray-Code
    '''
    elite = population[np.argmax(fitness)]
    neue_population = []
    while len(neue_population) < population_size:
        kandidaten = np.random.randint(0, population_size, 2)
        gewinner = (kandidaten[0] if fitness[kandidaten[0]] >= fitness[kandidaten[1]]
                    else kandidaten[1])
        neue_population.append(population[gewinner])
    return elite, np.array(neue_population)


def roulette_selektion(population, fitness):
    '''
    Erstellung einer neuen Population durch Auswahl der Individuen mit Rouletteselektion
    :param population: String numpy array bestehend aus Individuen (x-Koordinaten) kodiert mit Gray-Code
    :param fitness: numpy array der Fitness jedes Individuums
    :return: Individuum mit höchster Fitness (String) und String numpy array der neuen population kodiert mit Gray-Code
    '''
    elite = population[np.argmax(fitness)]
    relative_fitness = fitness / np.sum(fitness)
    neue_population = np.random.choice(population, population_size, p=relative_fitness)
    return elite, neue_population


def rekombination(population):
    '''
    return der neuen Population nach der Rekombination (Crossover) der Individuen
    :param population: String numpy array bestehend aus Individuen (x-Koordinaten) kodiert mit Gray-Code
    :return: String numpy array der Individuen der neuen Population kodiert mit Gray-Code
    '''
    for i in range(0, population_size, 2):
        kind1, kind2 = population[[i, i+1]]
        cross_punkt = np.random.randint(1, 4) if random.random() <= p_c else 0
        population[i] = kind1[:cross_punkt] + kind2[cross_punkt:]
        population[i+1] = kind2[:cross_punkt] + kind1[cross_punkt:]
    return population


def mutation(population):
    '''
    return der neuen Population nach Mutationen
    :param population: String numpy array bestehend aus Individuen (x-Koordinaten) kodiert mit Gray-Code
    :return: String numpy array der Individuen der neuen Population kodiert mit Gray-Code
    '''
    for x, individuum in enumerate(population):
        for i, bit in enumerate(individuum):
            if random.random() <= p_m:
                new_bit = "0" if bit == "1" else "1"
                individuum = individuum[:i] + new_bit + individuum[i+1:]
        population[x] = individuum
    return population


def kodieren(dez):
    '''
    Kodierung einer Dezimalzahl zu Gray-Code
    :param dez: Dezimalzahl
    :return: String des Gray-Code
    '''
    dez ^= (dez >> 1)
    return format(dez, '#017b')[2:]


def dekodieren(gray):
    '''
    Dekodierung von Gray-Code zu einer Dezimalzahl
    :param gray: String einer Zahl dargestellt mit Gray-Code
    :return: int Dezimalzahl
    '''
    dez = int(gray, 2)
    mask = dez
    while mask != 0:
        mask >>= 1
        dez ^= mask
    return dez * 31 / ((2 ** 15) - 1)  # Umrechnungsfaktor auf das Intervall [0,31]

if __name__ == "__main__":
    finale_population = genetischer_algorithmus(plotting=True)
    print(np.round(finale_population, 2))  # Ausgabe aller Individuen der letzten Generation

