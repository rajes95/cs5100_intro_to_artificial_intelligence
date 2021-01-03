'''
svm_iris.py

Iris flower classification using an SVM model.

@author: Rajesh Sakhamuru
@version: 11/25/2019
'''
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd


def main():

    colnames = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

    # import data file
    try:
        irisData = pd.read_csv("Iris/iris.data", names=colnames)
    except:
        print("File not found")
        exit(-1)

    print(irisData)

    # separate data into 'x' which is all attribute data, and flower label data 'y'
    x = irisData.drop('class', axis=1)
    y = irisData['class']

    # Split data into training and testing data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5)

    # linear kernel
    irisClassifier = SVC(kernel='linear')

    # polynomial kernel
#     irisClassifier = SVC(kernel='poly',degree=8)

    # gaussian kernel
#     irisClassifier = SVC(kernel='rbf')

    # Train model
    irisClassifier.fit(x_train, y_train)

    # TESTING model
    y_pred = irisClassifier.predict(x_test)

    print("\n", confusion_matrix(y_test, y_pred))

    print(classification_report(y_test, y_pred))

    return


main()

