import matplotlib.pyplot as plt
import numpy as np


def plotte_generationen(population, titel):
    '''
    Erstellung von einem Graphen zur Darstellung der Funktion und Individuen einer Population
    :param population: numpy array bestehend aus Individuen (x-Koordinaten) codiert mit Gray-Code
    :param titel: String des Graphtitels
    '''
    from main import dekodieren, berechne_fitness
    x = np.linspace(0, 31, 200)
    y = 0.0054 * pow(x, 3) - 0.23 * pow(x, 2) + 2.5 * x
    plt.plot(x, y)  # plotte die Funktion
    plt.vlines(31, -3, 17.5, 'r')
    plt.vlines(0, -3, 17.5, 'r')
    plt.xlabel('x')
    plt.ylabel('y')

    xwerte = list(np.array([dekodieren(i) for i in population]))
    ywerte = berechne_fitness(population)
    w = [xwerte.count(i) * 10 for i in xwerte]
    plt.scatter(xwerte, ywerte, w)  # plotte die Individuen
    plt.title(titel)
    plt.show()


def plotte_optimum(eliten):
    '''
       Erstellung von einem Graphen zur Darstellung der Entferung zum Optimum in Abhängigkeit der
       Generation
       :param eliten: numpy array bestehend aus dem besten Individuum (x-Koordinat) jeder Generation
       codiert mit Gray-Code
       '''
    from main import generationen, berechne_fitness
    y = np.round(berechne_fitness(eliten), 2)
    plt.plot(range(0, generationen), 17.3414 - y)  # Das Optimum ist 17,3414
    plt.xlabel('Generation')
    plt.ylabel('Entfernung zum Optimum')
    plt.title('Qualität der besten Lösungskandidaten')
    plt.show()

if __name__ == "__main__":
    plotte_generationen()