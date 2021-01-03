'''
svm_mushroom.py

Edible vs Poisonous mushroom classification using an SVM model.

@author: Rajesh Sakhamuru
@version: 11/26/2019
'''
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd


def main():

    colnames = ['class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises?', 'odor',
                'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
                'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
                'stalk-surface-below-ring', 'stalk-color-above-ring',
                'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
                'ring-type', 'spore-print-color', 'population', 'habitat']

    try:
        data = open("Mushroom/agaricus-lepiota.data", 'r')
        new = open("Mushroom/numericMushroom.data", 'w')
    except:
        print("File not found")
        exit(-1)
    # generate a new datafile where all data is assigned a numeric value instead of
    # arbitrary category labels so that the SVM model can plot the data in n-dimentional
    # hyperspace
    for line in data:
        for l in line:
            if l != "," and l != "\n":
                new.write(str(ord(l)))
            elif l != "\n":
                new.write(",")

        new.write("\n")

    data.close()
    new.close()

    try:
        shroomData = pd.read_csv("Mushroom/numericMushroom.data", names=colnames)
    except:
        print("File not found")
        exit(-1)

    print(shroomData)

    # separate data into 'x' which is all attribute data, and mushroom label data 'y'
    x = shroomData.drop('class', axis=1)
    y = shroomData['class']

    # Split data into training and testing data (50/50 split)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5)

    # linear kernel
    shroomClassifier = SVC(kernel='linear')

    # polynomial kernel
#     shroomClassifier = SVC(kernel='poly',degree=8)

    # gaussian kernel
#     shroomClassifier = SVC(kernel='rbf')

    # Train model using 50% of available data
    print("\nFitting model.....")
    shroomClassifier.fit(x_train, y_train)

    # TESTING model using other 50% of available data
    y_pred = shroomClassifier.predict(x_test)

    print("\n", confusion_matrix(y_test, y_pred))

    print("\n101 => Edible\n112 => Poisonous\n")
    # analyze prediction data vs actual data
    print(classification_report(y_test, y_pred))

    return


main()

