'''
ANN_iris.py

Artificial Neural Network to predict poisonous vs edible mushrooms

@author: Rajesh Sakhamuru
@version: 11/26/2019
'''

from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense


def main():


    # open file to read original data and then convert every column to
    # integer values in a new data file.
    # edible is 0 and poisonous is 1
    try:
        data = open("Mushroom/agaricus-lepiota.data", 'r')
        new = open("Mushroom/numericMushroom.data", 'w')
    except:
        print("File not found")
        exit(-1)

    for line in data:
        first = True
        for l in line:
            if first:
                if l == 'e':
                    new.write('0')
                    first = False
                else:
                    new.write('1')
                    first = False
            elif l != "," and l != "\n":
                new.write(str(ord(l)))
            elif l != "\n":
                new.write(",")

        new.write("\n")

    data.close()
    new.close()

    try:
        irisData = loadtxt("Mushroom/numericMushroom.data", delimiter=',')
    except:
        print("File not found")
        exit(-1)

    # separate data into 'x' which is all attribute data, and mushroom label data 'y'
    x = irisData[:, 1:23]
    y = irisData[:, 0]

    # Define Keras Model. input_dim is number of attributes. Output is binary (0/1)
    # representing edible/poisonous
    model = Sequential()
    model.add(Dense(22, input_dim=22, activation='relu'))
    model.add(Dense(11, activation='relu'))
    model.add(Dense(11, activation='relu'))
    model.add(Dense(11, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Compile Keras model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    print("Fitting model..... (please wait)")
    model.fit(x, y, epochs=200, batch_size=100, verbose=0)

    # make predictions using just attribute data
    predictions = model.predict_classes(x)

    # the first 10 cases predictins
    print("\nFirst 10 cases predicted vs expected:")
    for i in range(10):
        print('%s => %d (expected %d)' % (x[i].tolist(), predictions[i], y[i]))

    print("\n0 => Edible\n1 => Poisonous\n")

    _, accuracy = model.evaluate(x, y)
    print('Accuracy: %.2f' % (accuracy * 100))

    return


main()

