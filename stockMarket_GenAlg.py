# Stock Market Analysis
# Description: Using Genetic Algorithms to make predictions on whether to buy
# or short stocks.
#


from yahoo_finance import Share
import numpy
import random

# Set the Constants ---------------
StartingDate = '2015-04-01'
EndingDate = '2016-04-14'
PopulationSize = 10
DataSize = 0
NumberOfGenerations = 0
MutationRate = 5
MutationChange = 2
#----------------------------------

class Chromosome():
   def __init__(self, min=None, max=None, prev_min=None, prev_max=None, buy=None, score =None):
        self.min = min
        self.max = max
        self.prev_min = prev_min
        self.prev_max = prev_max
        self.buy = buy
        self.score = score

class TrainingData(object):
    population = []
    nextGeneration = []
    dayChange = []
    nextDayChange = []
    profit = []

    def generateData(self):
        global StartingDate
        global EndingDate
        global DataSize
        stock = Share('AAPL')
        data = stock.get_historical(StartingDate,EndingDate)
        file = open('stock_data', 'w')
        closes = [c['Close'] for c in data]
        opens = [o['Open'] for o in data]
        oArray = []
        cArray = []

        for c in closes:
            cArray.append(c)

        for o in opens:
            oArray.append(o)

        for x in range(len(data)-2):
            #  %Difference, Next Day %Difference, Money Made Holding for a Day
            file.write(str((float(cArray[x])-float(oArray[x+1]))/100) + ' ' + str((float(cArray[x+1]) - float(oArray[x+2]))/100) + ' ' + str((float(oArray[x]) - float(oArray[x+1]))) + '\n')

            self.dayChange.append((float(cArray[x])-float(oArray[x+1]))/100)
            self.nextDayChange.append(float(cArray[x+1]) - float(oArray[x+2])/100)
            self.profit.append(float(oArray[x]) - float(oArray[x+1]))
        #Makes sure the population size is
        DataSize = len(self.dayChange)
        file.close()

    def populationInit(self):

        #Create N Chromosomes with N being the Population Size
        #Each variable of Chromosome is assigned a number from a normal distribution
        #with the mean being 0 and the Standard Deviation being 1.5

        mu, sigma = 0, 0.15 # mean and standard deviation
        s = numpy.random.normal(mu, sigma, 4*PopulationSize)
        x = iter(s)
        for i in range(PopulationSize):
            temp = Chromosome(x.next(),x.next(),x.next(),x.next(),random.randint(0,999)%2, 0)

            #If the mininum is assigned a higher value than the max swap them
            #so that it makes sense.
            if temp.min > temp.max:
                temp.min, temp.max = temp.max, temp.min
            if temp.prev_min > temp.prev_max:
                temp.prev_min, temp.prev_max = temp.prev_max, temp.prev_min

            #Push the Chromosome into the population array.
            self.population.append(temp)


    def fitnessFunction(self):
        for i in range(PopulationSize):
            match = False
            for j in range(DataSize):
                #If match is found we BUY
                if(self.population[i].prev_min < self.dayChange[j] and self.population[i].prev_max > self.dayChange[j]):
                    if(self.population[i].min < self.nextDayChange[j] and self.population[i].max > self.nextDayChange[j]):
                        if(self.population[i].buy == 1):
                            match = True
                            self.population[i].score += self.profit[j]

                #Match is found and we short
                if(self.population[i].prev_min < self.dayChange[j] and self.population[i].prev_max > self.dayChange[j]):
                    if(self.population[i].min < self.nextDayChange[j] and self.population[i].max > self.nextDayChange[j]):
                        if(self.population[i].buy == 0):
                            match = True
                            self.population[i].score -= self.profit[j]

                #We have not found any matches = -5000
                if match == False:
                    self.population[i].score = -5000

    def weighted_random_choice(self):
        self.fitnessFunction()
        max = sum(self.population.score for self.population in self.population)
        pick = random.uniform(0,max)
        current = 0
        for i in range(len(self.population)):
            current += self.population[i].score
            if current > pick:
                return self.population[i]


class GeneticAlgorithm(object):
    pass

if __name__ == '__main__':
    x = TrainingData()
    x.generateData()
    x.populationInit()

