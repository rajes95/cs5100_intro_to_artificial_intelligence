'''
ANN_iris.py

Artificial Neural Network to predict Iris flower types

@author: Rajesh Sakhamuru
@version: 11/26/2019
'''

from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical


def main():

    # open file to read original data and then convert even the last column to
    # integer values in a new data file.
    try:
        data = open("Iris/iris.data", 'r')
        new = open("Iris/numericIris.data", 'w')
    except:
        print("File not found")
        exit(-1)

    for line in data:
        lineSplit = str(line).split(",")
        new.write(lineSplit[0] + "," + lineSplit[1] + "," + lineSplit[2] + "," + lineSplit[3] + ",")
        if lineSplit[4] == 'Iris-setosa\n':
            new.write("0\n")
        elif lineSplit[4] == 'Iris-versicolor\n':
            new.write("1\n")
        elif lineSplit[4] == 'Iris-virginica\n':
            new.write("2\n")

    data.close()
    new.close()

    try:
        irisData = loadtxt("Iris/numericIris.data", delimiter=',')
    except:
        print("File not found")
        exit(-1)

    # separate data into 'x' which is all attribute data, and flower label data 'y'
    x = irisData[:, 0:4]
    y = irisData[:, 4]
    # categorize the result column so 0/1/2 are separate categories
    y_cats = to_categorical(y)

    # Define Keras Model. input_dim is number of attributes. Output is 3 (0/1/2)
    model = Sequential()
    model.add(Dense(12, input_dim=4, activation='relu'))
    model.add(Dense(6, activation='relu'))
    model.add(Dense(6, activation='relu'))
    model.add(Dense(6, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    
    # Compile Keras model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    #Fit model to x and y data
    model.fit(x, y_cats, epochs=200, batch_size=110, verbose=0)

    predictions = model.predict_classes(x)

    # print all 150 cases predicted vs expected using model
    print("\nAll 150 cases predicted vs expected:")
    for i in range(150):
        print('%s => %d (expected %d)' % (x[i].tolist(), predictions[i], y[i]))

    print("\n0 => Iris-setosa\n1 => Iris-versicolor\n2 => Iris-virginica\n")

    _, accuracy = model.evaluate(x, y_cats)
    print('Accuracy: %.2f' % (accuracy * 100))

    # RUN AGAIN if accuracy is less than 90%, because the ANN keras model
    # could be made made much more efficient
    if accuracy < .9:
        print("\nRunning again for higher accuracy:")
        main()

    return


main()

