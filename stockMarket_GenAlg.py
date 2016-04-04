# Stock Market Analysis
# Description: Using Genetic Algorithms to make predictions on whether to buy
# or short stocks.
#


from yahoo_finance import Share
import string
import numpy
import random

# Set the Constants ---------------
StartingDate = '2015-01-01'
EndingDate = '2016-04-01'
PopulationSize = 200
NumberOfGenerations = 50
MutationRate = 5
MutationChange = 2
#----------------------------------

class Chromosome():
   def __init__(self, min=None, max=None, prev_min=None, prev_max=None, buy=None):
        self.min = min
        self.max = max
        self.prev_min = prev_min
        self.prev_max = prev_max
        self.buy = buy

class TrainingData():
    dayChange = []
    nextDayChange = []
    profit = []
    population = []

    def createData(self):
        startDate = '2015-6-01'
        endDate = '2016-01-01'
        stock = Share('AAPL')
        data = stock.get_historical(startDate,endDate)
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

            TrainingData.dayChange.append((float(cArray[x])-float(oArray[x+1]))/100)
            TrainingData.nextDayChange.append(float(cArray[x+1]) - float(oArray[x+2])/100)
            TrainingData.profit.append(float(oArray[x]) - float(oArray[x+1]))

        file.close()

    def populationInit(self):

        #Create N Chromosomes with N being the Population Size
        #Each variable of Chromosome is assigned a number from a normal distribution
        #with the mean being 0 and the Standard Deviation being 1.5

        mu, sigma = 0, 0.15 # mean and standard deviation
        s = numpy.random.normal(mu, sigma, 4*PopulationSize)
        x = iter(s)
        for i in range(PopulationSize):
            temp = Chromosome(x.next(),x.next(),x.next(),x.next(),random.randint(0,999)%2)

            #If the mininum is assigned a higher value than the max swap them
            #so that it makes sense.
            if temp.min > temp.max:
                temp.min, temp.max = temp.max, temp.min
            if temp.prev_min > temp.prev_max:
                temp.prev_min, temp.prev_max = temp.prev_max, temp.prev_min

            #Push the Chromosome into the population array.
            TrainingData.population.append(temp)
            #print()

    def fitnessFunction(self):
        print('fitness')


    #createData(object)
    populationInit(object)

class GeneticAlgorithm(object):
    def PopulationInit(self):
       print("hi")

if __name__ == '__main__':
    x = TrainingData