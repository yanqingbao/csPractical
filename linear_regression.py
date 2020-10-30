import csv
import random
import math
import operator
import pandas as pd
import numpy as np

'''
Functional: 
    1. train/test splitting
    2. fitting the model
    3. running prediciton on the holdout dataset (Test dataset)
    4. Function for outputting some analysis (organized text)
    5. print the MSE
'''


class Dataloader:
    def __init__(self, path):
        self.data = pd.read_csv(path)
        self.length = len(self.data)
        self.drop_address()
        self.feature, self.label = self.get_feature_label()
        self.train_test_split(0.8)
        self.normalize()
        self.bias()

    def drop_address(self): # drop the address column in the dataset
        self.data.drop(columns = 'Address', inplace = True)


    def get_feature_label(self):
        feature = self.data.iloc[:, : -1]
        label = self.data.iloc[:, -1]

        return (feature, label)

    def train_test_split(self, train_ratio = 0.7):
        self.train_mask = [random.randint(1, 100) < (100 * train_ratio) for i in range(self.length)]
        self.test_mask = [not i for i in self.train_mask]

    def normalize(self):
        self.train_features = self.feature[self.train_mask]
        self.train_labels = self.label[self.train_mask]

        self.train_min = np.min(self.train_features, axis = 0)
        self.train_max = np.max(self.train_features, axis = 0)

        self.train_features = (self.train_features - self.train_min) / (self.train_max - self.train_min)

        self.test_features = self.feature[self.test_mask]
        self.test_labels = self.label[self.test_mask]
        
        self.test_features = (self.test_features - self.train_min) / (self.train_max - self.train_min)

    def bias(self): # add a columns of ones as features
        self.train_features['bias'] = 1
        self.test_features['bias'] = 1


    def train_val_split(self):
        return ((self.train_features, self.train_labels) , (self.test_features, self.test_labels))

    def plot_corr(self):
        return 42


class LinearRegression:
    def __init__(self, path='./USA_Housing.csv'):
        self.dataloader = Dataloader(path)
        self.train, self.val = self.dataloader.train_val_split()

        self.train_features, self.train_labels = self.train
        self.test_features, self.test_labels = self.val


    def fit(self): # (X^T X)^-1 X^T Y
        from numpy.linalg import inv
        from numpy import matmul, transpose
        self.beta = inv(self.train_features.transpose().dot(self.train_features))
        self.beta = matmul(self.beta, transpose(self.train_features))
        self.beta = matmul(self.beta, self.train_labels)


    def get_mse(self):
        self.pred_labels = np.matmul(self.test_features, self.beta)
        self.mse = np.mean(np.square(self.pred_labels - self.test_labels), axis = 0)

        from sklearn.linear_model import LinearRegression
        reg = LinearRegression().fit(self.train_features, self.train_labels)
        self.sk_mse = np.mean(np.square(reg.predict(self.test_features) - self.test_labels), axis = 0)

        return (self.mse, self.sk_mse)
if __name__ == '__main__':
    lr = LinearRegression()
    lr.fit()
    lr_mse, sk_lr_mse = lr.get_mse()
    print(f'Our Linear Regression Model MSE:\n{lr_mse}\nScikit-learn LR Model MSE: \n{sk_lr_mse}')





'''
Task

Train a linear regression model from this dataset. If you are not familiar with Kaggle you can also download the dataset here.

Background:

Linear Regression is a way of predicting a response Y on the basis of a single predictor variable X. It is assumed that there is approximately a linear relationship between X and Y. Mathematically, we can represent this relationship as:
Y ≈ ɒ + ß X + ℇ
where ɒ and ß are two unknown constants that represent intercept and slope terms in the linear model and ℇ is the error in the estimation.
Steps:

Start by taking the simplest possible example and alculate the regression with only two data points (price for dependent and number of rooms for independent).

Then use price as the dependent variable and all others as independent variables.

Functional statements

Function for train/test splitting
Function for fitting the model
Function for running prediction on the holdout (test) set
Function for outputting some analysis (organized text here is fine)
Output

Lastly, print the mean squared error of your results
BONUS STEPS:

Explore the correlation using Pearson Correlation Coefficient. If you want resources for this check out the pandas implementation or the Wiki article
Re-implement Seaborn's library for plotting pairwise relationships in a dataset

'''