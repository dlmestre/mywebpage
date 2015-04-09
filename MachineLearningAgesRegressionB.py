import numpy as np
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
from sklearn import linear_model

import pandas as pd

train_path = r"/home/david/Documents/train_file_ages.csv"
test_path = r"/home/david/Documents/test_file_ages.csv"

def studentReg(x, y):
    ### training regression

    x = np.array(x)
    y = np.array(y)
    clf = linear_model.LinearRegression()
    reg = clf.fit(x[:,np.newaxis], y)
    
    return reg

def results():
    
    data_train = pd.read_csv(train_path)
    ages_train = data_train["ages_train"].tolist()
    net_worths_train = data_train["net_worths_train"].tolist()
    
    data_test = pd.read_csv(test_path)
    ages_test = data_test["ages_test"].tolist()
    net_worths_test = data_test["net_worths_test"].tolist()
    
    return ages_train, net_worths_train, ages_test, net_worths_test

def classifier():
    ages_train, net_worths_train, ages_test, net_worths_test = results()
    
    reg = studentReg(ages_train, net_worths_train)
    
    ages_test = np.array(ages_test)

    plt.clf()
    plt.scatter(ages_train, net_worths_train, color="b", label="train data")
    plt.scatter(ages_test, net_worths_test, color="r", label="test data")
    plt.plot(ages_test, reg.predict(ages_test[:,np.newaxis]), color="black") #predict(ages_test[:,np.newaxis])
    plt.legend(loc=2)
    plt.xlabel("ages")
    plt.ylabel("net worths")
    plt.show()
