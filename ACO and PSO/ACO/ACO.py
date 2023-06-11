import random
from  ACO_fileRead import FileRead
from Ant import Ant
import math
import matplotlib.pyplot as plt
import numpy as np


class AntColonyOptimization:
    def __init__(self, alpha, beta, iteration, numAnts, evapRate, path) -> None:
        self.alpha = alpha
        self.beta = beta
        self.iteration = iteration
        self.numAnts = numAnts
        self.evapRate = evapRate
        self.Q = 1
        temp = FileRead(path)
        fileInst = temp.instanceTaker()
        self.capacity = fileInst["capacity"]
        self.depot = fileInst["depot"][0]
        self.dimension = fileInst["dimension"]
        self.demand = fileInst["demand"]
        self.distaneMatrix = fileInst["edge_weight"]       
        self.inverseDM = [[1/i if i != 0 else 0 for i in lst] for lst in self.distaneMatrix]
        self.path = path

    def AntMaking(self):
        fullRoute = []
        unvisited = [i for i in range(1, self.dimension)]
        currentCity = self.depot
        truckCapacity = self.capacity
        totalDistance = 0
        tempRoute = []
        tempRoute.append(self.depot)
        while len(unvisited) >= 1:
            # Choosing random city from unvisited cities
            tempCity = random.randint(0, len(unvisited) - 1)
            city = unvisited[tempCity]
            if self.demand[city] <= truckCapacity:
                truckCapacity -= self.demand[city]
                totalDistance += self.distaneMatrix[currentCity][city]
                currentCity = city
                tempRoute.append(city)
                # Now its time to pop the city from unvisited
                unvisited.pop(tempCity)
            else:
                # This means that the truck is full and we need to go back to depot and line 70 will simply add the distance of depot to current city or vice versa
                totalDistance += self.distaneMatrix[currentCity][0]
                fullRoute.append(tempRoute)
                # Changing the capacity of vehicles
                truckCapacity = self.capacity
                tempRoute = []
                tempRoute.append(self.depot)
                currentCity = self.depot
                truckCapacity -= self.demand[city]
                totalDistance += self.distaneMatrix[currentCity][city]
                currentCity = city
                tempRoute.append(city)
                unvisited.pop(tempCity)

        # Now I have to go back to depot to complete the route
        tempRoute.append(self.depot)
        totalDistance += self.distaneMatrix[currentCity][0]
        fullRoute.append(tempRoute)
        antObject = Ant(fullRoute, totalDistance)        
        return antObject


    def AntColonyInitialization(self):
        # Initalizing Pheromones with 1
        self.numNodes = len(self.distaneMatrix)
        self.pheromones = [[0 for i in range(self.numNodes)] for j in range(self.numNodes)]
        self.ants = [0 for i in range(self.numAnts)]

        # Making Artificial Ants by calculating Routes
        self.ants = []
        for i in range(self.numAnts):
            temp = self.AntMaking()
            self.ants.append(temp)
       

    def computingDeltaT(self):
        deltaT = [[0 for i in range(self.dimension)] for j in range(self.dimension)]
        for ant in self.ants:
            for route in ant.routes:
                for path in range(0,len(route)-1):
                    deltaT[route[path]][route[path+1]] += 1/ant.distance
                    # deltaT[route[path+1]][route[path]] += 1/ant.distance
        return deltaT
    

    def calculateProbabilities(self, possibleCities, currentCity):

        probCities = []
        for i in possibleCities:
            temp = math.pow(self.Tau[currentCity][i], self.alpha) + math.pow(self.inverseDM[currentCity][i], self.beta)
            probCities.append(temp)
        sumProb = sum(probCities)
        finalProb = [i/sumProb for i in probCities]

        # Now making the ranges of Probabilities
        probRange = {}
        startRange = 0
        for i in range(len(finalProb)):
            probRange[i] = [startRange , startRange + finalProb[i]]
            startRange += finalProb[i]        
        return probRange



    def simulateAnt(self):
        # Copying the code from AntMaking as now I have to decide the city with the help of probabilities
        fullRoute = []
        unvisited = [i for i in range(self.dimension)]
        currentCity = self.depot
        truckCapacity = self.capacity
        totalDistance = 0
        tempRoute = []
        tempRoute.append(self.depot)

        while len(unvisited) >1:
            # Choosing random city from unvisited cities
            possibCities = []
            for i in unvisited:
                if self.demand[i] <= truckCapacity and i!= currentCity:
                    possibCities.append(i)
            
            probRange = self.calculateProbabilities(possibCities, currentCity)
            randNum = random.random()
            for i in probRange:
                if randNum >= probRange[i][0] and randNum <= probRange[i][1]:
                    selectedCity = i
                    break            
            nextCity = possibCities[selectedCity]
            truckCapacity -= self.demand[nextCity]
            totalDistance += self.distaneMatrix[currentCity][nextCity]
            currentCity = nextCity
            tempRoute.append(currentCity)
            if currentCity == self.depot:
                truckCapacity = self.capacity
                fullRoute.append(tempRoute)
                tempRoute = [self.depot]
            else:
                for i in unvisited:
                    if i == nextCity:
                        unvisited.remove(i)
                        break

        # Now the path will again go to Depot to make a full route
        tempRoute.append(self.depot)
        totalDistance += self.distaneMatrix[currentCity][0]
        fullRoute.append(tempRoute)
        return Ant(fullRoute, totalDistance)



    def updatePhermone(self):
        DeltaT = self.computingDeltaT()
        for i in range(len(self.Tau)):
            for j in range(len(self.Tau)):
                self.Tau[i][j] = (self.Tau[i][j] * self.evapRate) + DeltaT[i][j]
            

    def ACO_main(self):
        self.AntColonyInitialization()
        # Updating the Tau Matrix
        self.Tau = self.computingDeltaT()
        minDist = float('inf')
        minDistanceList = []
        avgDistanceList = []
        for i in range(self.iteration):
            tempAnt = []
            avgDistance = 0
            for j in range(self.numAnts):
                tempAnt.append(self.simulateAnt())
            self.ants = tempAnt
            self.updatePhermone()
            for ant in self.ants:
                if ant.distance < minDist:
                    minDist = ant.distance
                    minRoute = ant.routes
                avgDistance += ant.distance
      
            avgDistance = avgDistance // self.numAnts
            minDistanceList.append(minDist)
            avgDistanceList.append(avgDistance)
        return minDistanceList, avgDistanceList, minDist

if __name__ == "__main__":
    temp = AntColonyOptimization(2, 3, 200, 10, 0.5, "A-n32-k5")
    result = temp.ACO_main()
    print(f'Minimum Distance is {result[2]}')






# Code for geenrating graph with repect to changing alpha beta gamma and evaporation rate
filename = "A-n32-k5"

# alpha = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# beta = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# evapRate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# iterations = 50
# AllResults = []
# for i in range(len(alpha)):
#     temp = AntColonyOptimization(alpha[i], beta[i], iterations, 10, evapRate[i], filename )
#     result = temp.ACO_main()
#     AllResults.append(result[0][-1])

# # Now I have to create a 4d graph using Matplot Lib

# print(AllResults)

