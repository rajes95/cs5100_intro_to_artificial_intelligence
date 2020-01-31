'''
hw10_K_means_clustering.py

classification of wine types based on k-means clustering

@author: Rajesh Sakhamuru
@version: 12/3/2019
'''

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def main():
    """
    The data is modified to replace the 1/2/3 classification of wine
    to 0/1/2 so the k-means cluster can better classify the wine.
    Otherwise it does not ever classify anything as wine "class 3."
    """
#     try:
#         data = open("data/wine.data", 'r')
#         new = open("data/editedWine.data", 'w')
#     except:
#         print("File not found")
#         exit(-1)
#
#     for line in data:
#         lineSplit = str(line).split(",")
#         if lineSplit[0] == '1':
#             new.write("0,")
#         elif lineSplit[0] == '2':
#             new.write("1,")
#         elif lineSplit[0] == '3':
#             new.write("2,")
#
#         for n in range(1,13):
#             new.write(lineSplit[n] + ",")
#         new.write(lineSplit[13])
#
#
#     data.close()
#     new.close()

    colnames = ['class', 'Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 'Magnesium',
                 'Total phenols', 'Flavinoids', 'Nonflavanoid phenols', 'Proanthocyanins',
                 'Color intensity', 'Hue', 'OD280/OD315', 'Proline']

    try:
        data = pd.read_csv("data/editedWine.data", names=colnames)
    except:
        print("File not found")
        exit(-1)

    x = np.array(data.drop(['class'], 1))
    y = np.array(data['class'])

    kmeans = KMeans(n_clusters=3, max_iter=500)

    kmeans.fit(x)

    correct = 0
    for i in range(len(x)):
        predict_me = np.array(x[i])
        predict_me = predict_me.reshape(-1, len(predict_me))
        prediction = kmeans.predict(predict_me)

        print("Predicted: " + str(prediction[0]) + " (Expected: " + str(y[i]) + ")")

        if prediction[0] == y[i]:
            correct += 1

    accuracy = correct / len(x)

    print("Clustering prediction accuracy: " + str(accuracy))

    return


main()

