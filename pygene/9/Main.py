#-*- coding: utf8 -*- 

"""
Implementacia problemu obchodneho cestujuceho (TSP)
"""

from pygene.gene import FloatGene, FloatGeneMax, FloatGeneRandom
from pygene.organism import Organism, MendelOrganism
from pygene.population import Population

"""
Nevyhnutne importy pre pouzitie pyGene
"""
import sys
from math import sqrt

width = 500
height = 500

"""
Pocet generacii genetickeho algoritmu
"""
numGenerations=100

"""
Konfiguracia
"""
geneRandMin = 0.0
geneRandMax = 10.0
geneMutProb = 0.1

"""
Ak sa nepouziva FloatGeneRandom
"""
geneMutAmt = .5        

popInitSize = 10
popChildCull = 20
popChildCount = 100

"""
Pocet rodicov, ktory sa budu pridavat do novej generacie
"""
popIncest = 10        

"""
Pravdepodobonost mutacie
"""
popNumMutants = 0.7     

"""
Pocet nahodnych organizmov pridanych do kazdej generacie
"""
popNumRandomOrganisms = 0 
mutateOneOnly = False
BaseGeneClass = FloatGene
BaseGeneClass = FloatGeneMax
#BaseGeneClass = FloatGeneRandom
OrganismClass = MendelOrganism
mutateAfterMating = True
"""
Pravdepodobnost krizenia
"""
crossoverRate = 0.05

"""
Kazdy gen reprezentuje prioritu cesty do daneho mesta
"""
class CityPriorityGene(BaseGeneClass):

    randMin = geneRandMin
    randMax = geneRandMax
    mutProb = geneMutProb
    mutAmt = geneMutAmt


"""
Trieda reprezentujuca jedno mesto jeho poradovym cislom a suradnicami.
Navyse pocita vzialenost z ineho mesta.
"""
class City:
    
    """
    Konstruktor vytvori objekt mesta
    """
    def __init__(self, order, x=None, y=None):
        self.order = order
        self.x = x
        self.y = y
        
    """
    Pocita vzdialenost z tohto mesta do ineho 
    """
    def __sub__(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx * dx + dy * dy)

    def __repr__(self):
        return "<City %s at (%.2f, %.2f)>" % (self.order, self.x, self.y)

if 1:
    cities = [] 
    f = open(sys.argv[1],'r')
    citycounter=0
    isy=False;
    x="x"
    y="y"
    for line in f.readlines():
        l=line.split("\r")
        if l[0]=='':
            citycounter+=1
            cities.append(City("%s"%citycounter,int(x),int(y)))
        else:
            if (isy==True):
                y=l[0]
                isy=False
            else:
                x=l[0]
                isy=True
    f.close()

cityOrders = [city.order for city in cities]

cityCount = len(cities)

cityDict = {}
for city in cities:
    cityDict[city.order] = city

priInterval = (geneRandMax - geneRandMin) / cityCount
priNormal = []
for i in xrange(cityCount):
    priNormal.append(((i+0.25)*priInterval, (i+0.75)*priInterval))

genome = {}
for order in cityOrders:
    genome[order] = CityPriorityGene

"""
Jeden pseudo organizmus reprezentuje riesenie problemu
obchodneho cestujuceho
"""
class TSPSolution(OrganismClass):
    genome = genome
    mutateOneOnly = mutateOneOnly
    crossoverRate = crossoverRate
    numMutants = 0.3

    """
    Vracia vzdialenost celej cesty - fitness hodnotu problemu
    """
    def fitness(self):
        distance = 0.0
        """
        Ziskanie objektov miest podla priority
        """
        sortedCities = self.getCitiesInOrder()

        """
        Zaciname prvym mestom a pocitame vzdialenosti k poslednemu
        """
        for i in xrange(cityCount - 1):
            distance += sortedCities[i] - sortedCities[i+1]
        
        """
        Pripocitame cestu k prvemu mestu (navrat)
        """
        distance += sortedCities[0] - sortedCities[-1]
        return distance


    """
    Vracia zoznam miest zoradenych podla hodnot
    priorit ziskanych z genov jednotlivych organizmov
    """
    def getCitiesInOrder(self):
        sorter = [(self[order], cityDict[order]) for order in cityOrders]
        """
        Zoradenie
        """
        sorter.sort()
        """
        Ziskanie jednotlivych miest
        """
        sortedCities = [tup[1] for tup in sorter]
        return sortedCities


    """
    Upravuje geny
    """
    def normalise(self):
        genes = self.genes
        for i in xrange(2):
            sorter = [(genes[order][i], order) for order in cityOrders]
            sorter.sort()
            sortedGenes = [tup[1] for tup in sorter]
            

"""
Objekt populacie organizmov
"""
class TSPSolutionPopulation(Population):
    initPopulation = popInitSize
    species = TSPSolution
    childCull = popChildCull
    """
    Pocet potomkov, ktory sa maju vytvorit po kazdej populacii
    """
    childCount = popChildCount
    """
    "incest" - Pocet najlepsich rodicov, ktory
    sa pridaju do nasledujucej generacie
    """
    incest = popIncest
    mutants = popNumMutants
    numNewOrganisms = popNumRandomOrganisms
    mutateAfterMating = mutateAfterMating


"""
Hlavna metoda programu
"""
def main():
    
    """
    Vytvorenie povodnej populacie
    """
    pop = TSPSolutionPopulation()
    
    """
    Samotna evolucia
    """
    i = 0
    while i<=numGenerations:
        pop.gen()
        print "%s" % (int(pop.best().fitness()))
        i += 1

    """
    Ziskanie najlepsieho organizmu
    """
    solution = pop.best()
    

    sortedCities = solution.getCitiesInOrder()
    
    f = open(sys.argv[2],'w')
    f.write("<center><div id=\"canvas\" style=\"position:relative;width:700px;height:700px;background:white;float:center;\"></div></center><script type=\"text/JavaScript\">var canvasDiv=document.getElementById(\"canvas\");var gr = new jsGraphics(canvasDiv);var col = new jsColor(\"red\");var pen = new jsPen(col,1);var col2 = new jsColor(\"black\");")
    to=True
    tox=None
    toy=None
    firstx=int(sortedCities[0].x)
    firsty=int(sortedCities[0].y)
    fromx=int(sortedCities[1].x)
    fromy=int(sortedCities[1].y)
    f.write("gr.drawLine(pen,new jsPoint("+str(firstx)+","+str(firsty)+"),new jsPoint("+str(fromx)+","+str(fromy)+"));\n")
    for city in sortedCities[2:]:
        if to==False:
            f.write("gr.drawLine(pen,new jsPoint("+str(fromx)+","+str(fromy)+"),new jsPoint("+str(tox)+","+str(toy)+"));\n")
            fromx=int(city.x)
            fromy=int(city.y)
        else:
            tox=int(city.x)
            toy=int(city.y)
            f.write("gr.drawLine(pen,new jsPoint("+str(fromx)+","+str(fromy)+"),new jsPoint("+str(tox)+","+str(toy)+"));\n")
            fromx=tox
            fromy=toy
    f.write("gr.drawLine(pen,new jsPoint("+str(tox)+","+str(toy)+"),new jsPoint("+str(firstx)+","+str(firsty)+"));\n")
    for city in sortedCities:
        f.write("gr.fillCircle(col2,new jsPoint("+str(city.x)+","+str(city.y)+"),4);\n")
    f.write("</script>")
    f.close()
    
if __name__ == '__main__':
    main()





