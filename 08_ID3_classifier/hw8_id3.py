'''
hw8_id3.py

@author: Rajesh Sakhamuru
@version: 11/17/2019
'''

import Chefboost as chef
import pandas as pd

def main():
    """
    This program reads the contacts.txt file which has all the data pertaining to
    soft/none contact lense decisions, and then uses the Chefboost library's ID3 
    algorithm to generate a 'rules.py' file in the outputs folder which contains a
    decision tree that can be used with new data to predict whether or not they should
    wear 'none' or 'soft' contact lenses.
    
    The data given is tested against the 'predicted' decisions to ensure that the
    tree is accurate for all 20 data points.
    """
    data = pd.read_csv("dataset/contacts.txt")
    
    print(data)

    print()
    config = {'algorithm':'ID3'}
    model = chef.fit(data,config)

    print()
    
    print("prediction  vs  actual")
    
    for index,instance in data.iterrows():
        prediction = chef.predict(model,instance)
        actual = instance['Decision']
        print("     ",prediction, " vs ", actual)
    
    
    return


main()

