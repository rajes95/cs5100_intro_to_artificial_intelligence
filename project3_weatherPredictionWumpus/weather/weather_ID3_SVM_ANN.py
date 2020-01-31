'''
weather_ID3_SVM_ANN.py

ID3, SVM and ANN models for predicting how good weather is for shooting an arrow
in the wumpus game using weather data. Data is in the weather.data file in the same
folder. All 3 algorithms vote to determine a final result.

@author: Rajesh Sakhamuru
@version: 11/25/2019
'''

import pandas as pd
import numpy as np
from numpy import loadtxt
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical




class WeatherClassify:

    def __init__(self):

        # takes original data file (with mixed data types) and creates a purely float one
        self.cleanData()

        # imports data file where all values are floats
        colnames = ['outlook', 'temperature', 'humidity', 'windy', 'play']
        try:
            weatherData = pd.read_csv("weather/numericWeather.data", names=colnames)
        except:
            print("File not found")
            exit(-1)

        # uses numeric data to fit decision tree, SVM and ANN predictive models
        self.weatherTree = self.decTree(weatherData)
        self.weatherSVM = self.svmModel(weatherData)
        self.weatherANN = self.annModel()
        return

    def predict(self, attributes):
        """
        All 3 models (ID3 tree, SVM and ANN) vote to determine final prediction.
        
        attributes must be an array of 4 numeric values representing the atributes of
        outlook, temperature, humidity and windy.
        
        Attributes:-
        Outlook:     115 = Sunny
                     111 = Overcast
                     114 = Rainy
                     
        Temperature: Numeric value in Farenheit
        
        Humidity:    Numeric % humidity
        
        Windy:       102 = False
                     116 = True
        --------
        Return:-
        Play:        0 = No
                     1 = Yes
        """
        tree = self.weatherTree.predict([attributes])
        svm = self.weatherSVM.predict([attributes])
        ann = self.weatherANN.predict_classes(np.array([attributes]))

        count = tree[0] + svm[0] + ann[0]

        if count < 2:
            return 0
        else:
            return 1

    def cleanData(self):
        """
        All data from original data file is converted to numerical values to be used
        to fit predictive models.
        """
        try:
            data = open("weather/weather.data", 'r')
            new = open("weather/numericWeather.data", 'w')
        except:
            print("File not found")
            exit(-1)

        for line in data:
            lineSplit = str(line).split(",")
            new.write(str(ord(lineSplit[0])) + "," + lineSplit[1] + "," + lineSplit[2] + "," + str(ord(lineSplit[3])) + "," + str(ord(lineSplit[4][0]))[2])
            new.write("\n")

        data.close()
        new.close()

        return

    def decTree(self, weatherData):
        """
        Generates an ID3 tree using SciKit-learn buit-in algorithm and the given
        data
        """
        # separate data into 'x' which is all attribute data, and flower label data 'y'
        # axis=1 indicates dropping a column
        x = weatherData.drop('play', axis=1)
        y = weatherData['play']

        weatherTree = DecisionTreeClassifier()
        weatherTree = weatherTree.fit(x, y)

    #     y_pred = weatherTree.predict(x)
    #     print("Accuracy:", metrics.accuracy_score(y, y_pred))

        return weatherTree

    def svmModel(self, weatherData):
        """
        Generates an SVM predictive model (2nd degree polynomial kernel) using 
        SciKit-learn buit-in algorithm and the given data
        """
        # separate data into 'x' which is all attribute data, and flower label data 'y'
        # axis=1 indicates dropping a column
        x = weatherData.drop('play', axis=1)
        y = weatherData['play']

        weatherSVM = SVC(kernel='poly', degree=2)
        weatherSVM.fit(x, y)

    #     y_pred = weatherSVM.predict(x)
    #     print("\n"+classification_report(y, y_pred))

        return weatherSVM

    def annModel(self):
        """
        Generates an ANN model using keras buit-in algorithm and the given
        data to predict shooting weather.
        """
        try:
            weatherData = loadtxt("weather/numericWeather.data", delimiter=',')
        except:
            print("File not found")
            exit(-1)

        x = weatherData[:, 0:4]
        y = weatherData[:, 4]

        y_cats = to_categorical(y)

        weatherANN = Sequential()

        weatherANN.add(Dense(8, input_dim=4, activation='relu'))
        weatherANN.add(Dense(8, activation='relu'))
        weatherANN.add(Dense(8, activation='relu'))
        weatherANN.add(Dense(2, activation='softmax'))

        weatherANN.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        weatherANN.fit(x, y_cats, epochs=200, batch_size=10, verbose=0)

#         predictions = weatherANN.predict_classes(x)
#     
#         print("\nFirst 14 cases predicted vs expected:")
#         for i in range(14):
#             print('%s => %d (expected %d)' % (x[i].tolist(), predictions[i], y[i]))

        _, accuracy = weatherANN.evaluate(x, y_cats, verbose=0)
#         print('Accuracy: %.2f' % (accuracy * 100))

        if accuracy < .6:
            self.annModel()

        return weatherANN


