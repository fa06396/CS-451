import pandas as pd
import math
import numpy as np
from neuron import Neuron
from sklearn import preprocessing
import random
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.preprocessing import StandardScaler


class winNeuronData:
    def __init__(self, WinNeuron, countryName) -> None:
        self.winNeuron = WinNeuron
        self.countryName = countryName


class self_organizing_maps:
    def __init__(self, dimension, path, radius, learningRate, numIteration) -> None:
        self.height = dimension[0]
        self.width = dimension[1]
        self.numNeurons = self.height * self.width
        self.path = path
        self.learningRate = learningRate
        self.inputData = []
        self.DataCleaning()
        self.features = len(self.inputData[0])
        self.neurons = Neuron.generateRandom(
            self.numNeurons, self.features, self.MinData, self.MaxData, self.height, self.width)
        self.MinData = 0
        self.MaxData = 0
        self.radius = radius
        self.numIterations = numIteration
        self.sigma = 3
        self.winNeuronList = []

    def DataCleaning(self):
        '''
        This function is used to clean the data and normalize it between 0 and 1

        parameters: 
        - self : mandatory parameter for all the functions in python


        returns:
        - None
        '''
        df = pd.read_csv(self.path)
        df = df.dropna()
        df = df.drop(columns=['RANK', 'Happiness score',
                     'Whisker-high', 'Whisker-low'])
        columns = ['Explained by: Social support',
                   'Explained by: Freedom to make life choices', 'Explained by: Generosity', 'Explained by: Perceptions of corruption',
                   ]
        for i in df.columns:
            if i in columns:
                df[i] = df[i].str.replace(',', '.')
            else:
                df[i] = df[i].str.replace(',', '')
        self.df = df
        # For data to be used effectively we have to normalize it between certain values and for that I have used this method I found at GeeksforGeeks
        # Reference = https://www.geeksforgeeks.org/data-normalization-with-pandas/
        tempDf = df.drop(columns=['Country'])
        scaler = MinMaxScaler()
        scaledDf = scaler.fit_transform(tempDf)
        self.MinData = scaledDf.min()
        self.MaxData = scaledDf.max()
        self.inputData = scaledDf

    def CalcDistance(self, input1, input2):
        '''
        This function is used to Elucidean calculate the distance between two inputs

        parameters:
        - self : mandatory parameter for all the functions in python
        - input1 : the first input
        - input2 : the second input

        returns:
        - result : the distance between the two inputs
        '''
        result = 0
        for i in range(len(input1)):
            result += math.pow(input1[i] - input2[i], 2)
        return result

    def winningNeuron(self, inputRow):
        '''
        This function is used to find the winning neuron by calculating the distance between the input and the weights of the neurons

        parameters:
        - self : mandatory parameter for all the functions in python
        - inputRow : the input row that is being used to find the winning neuron
        - inputRowIndex : the index of the input row

        returns:
        - self.winNeuron : the winning neuron (Only for later Data Visualization)
        '''
        lowDist = math.inf
        for i in self.neurons:
            if self.CalcDistance(i.weights, inputRow) < lowDist:
                self.winNeuron = i
                lowDist = self.CalcDistance(i.weights, inputRow)

        return self.winNeuron

    def bestMatchingUnit(self, inputRow, winNeuronPos):
        '''
        used to find the best matching unit by calculating the distance between the input and all surronding neurons. The one who are more close are adjusted more than the ones who are far away

        parameters:
        - self : mandatory parameter for all the functions in python
        - inputRow : the input row that is being used to find the best matching unit
        - winNeuronPos : the position of the winning neuron


        returns:
        - None
        '''
        for i in range(len(self.neurons)):
            tempNeuron = (self.neurons[i].xloc, self.neurons[i].yloc)
            distance_to_bmu = self.CalcDistance(winNeuronPos, tempNeuron)
            neighborhood = math.exp(-distance_to_bmu**2 / (2 * self.sigma**2))
            for j in range(len(self.neurons[i].weights)):
                self.neurons[i].weights[j] = self.neurons[i].weights[j] + \
                    self.learningRate * neighborhood * \
                    (inputRow[j] - self.neurons[i].weights[j])

    def trainingSOM(self):
        '''
        This function is used to train the self organizing map by finding winning neuron and best matching unit

        parameters:
        - self : mandatory parameter for all the functions in python

        returns:
        - None
        '''
        for i in range(self.numIterations):
            for inputRow in range(len(self.inputData)):
                self.winningNeuron(self.inputData[inputRow])
                winPos = (self.winNeuron.xloc, self.winNeuron.yloc)
                self.bestMatchingUnit(self.inputData[inputRow], winPos)
            self.learningRate *= 0.9
            self.sigma *= 0.9

    def somGrid(self, activated):
        '''
        This function is used to plot the grid of the self organizing map

        There are few of the major changes taken from ChatGPT's code. The link to his code is given below in the References Section: 


        parameters:
        - self : mandatory parameter for all the functions in python
        - activated : the activation function that is being used

        returns:
        - None
        '''

        self.colorGrid = {}
        figure = plt.figure(figsize=(self.height, self.width))
        ax = figure.add_subplot(111, aspect='equal')
        plt.rcParams.update({'font.size': 6})

        for row in range(self.height):
            for column in range(self.width):
                temp = row*self.width + column
                weights = self.neurons[temp].weights
                rgb = [0, 0, 0]
                ax.set_xlim((0, self.width))
                ax.set_ylim((0, self.height))
                for i in range(len(weights)):
                    if i % 3 == 0:
                        rgb[0] = rgb[0] + weights[i] * activated
                    elif i % 3 == 1:
                        rgb[1] = rgb[1] + weights[i] * activated
                    else:
                        rgb[2] = rgb[2] + weights[i] * activated

                # Normalizing the rgb values
                rgbSum = sum(rgb)
                for i in range(len(rgb)):
                    rgb[i] = rgb[i]/rgbSum
                self.rgb = rgb
                # Plotting the grid
                ax.add_patch(plt.Rectangle((row, column), 1, 1, facecolor=(
                    rgb[0], rgb[1], rgb[2], 1), edgecolor='black'))
                self.colorGrid[(row, column)] = rgb

    def colorMap(self, activated):
        '''
        This function is used to plot the color map of the self organizing map with the countries

        There are few of the major changes taken from ChatGPT's code. The link to his code is given below in the References Section:

        parameters:
        - self : mandatory parameter for all the functions in python

        returns:
        - None
        '''

        gridData = []
        self.colourMatch = {}
        for i in range(len(self.inputData)):
            winNeuron = self.winningNeuron(self.inputData[i])
            self.winNeuronList.append(winNeuronData(
                winNeuron, self.df.loc[i, "Country"]))

        for i in range(len(self.winNeuronList)):
            countryName = self.winNeuronList[i].countryName
            winNeuron = self.winNeuronList[i].winNeuron
            self.colourMatch[countryName] = self.colorGrid[winNeuron.xloc,
                                                           winNeuron.yloc]
            centerx = winNeuron.xloc + activated
            centery = winNeuron.yloc + activated
            counter = 0
            while (centerx, centery) in gridData and counter < 4:
                centery = centery + activated
                counter += 1
            gridData.append((centerx, centery))
            plt.text(centerx, centery, countryName)
        plt.xlabel('Width')
        plt.ylabel('Height')
        plt.title('Self Organizing Map Grid View Visualization with Countries')
        plt.show()

    def mapVisualization(self):
        '''
        This function is used to plot the worldMap map with the countries

        There are few of the major changes taken from ChatGPT's code. The link to his code is given below in the References Section:

        parameters:
        - self : mandatory parameter for all the functions in python

        returns:
        - None
        '''

        worldMap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        fig, ax = plt.subplots(figsize=(10, 10))
        worldMap.plot(ax=ax, facecolor='lightgray', edgecolor='black')
        for i in self.colourMatch:
            color = self.colourMatch[i]
            if i in worldMap["iso_a3"].tolist():
                worldMap[worldMap.iso_a3 == i].plot(color=color, ax=ax)
        plt.show()

    def mainSOM(self):
        '''
        This function is used to call all the functions that are needed to run the SOM

        parameters:
        - self : mandatory parameter for all the functions in python

        returns:
        - None
        '''
        self.trainingSOM()
        self.somGrid(activated=0.7)
        self.colorMap(activated=0.2)
        self.mapVisualization()


if __name__ == "__main__":
    a = self_organizing_maps((40, 40), 'happyData.csv', 1, 1, 50)
    a.mainSOM()
