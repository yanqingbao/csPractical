import csv
import random
import math
import operator
import pandas as pd

import heapq

class kNN:

    def __init__(self, data , k=10):
        self.data = data
        self.k = k
        self.num = data.shape[0]
    
    def split_dataset(self, train_r = 0.7):
        self.train_mask = [random.randint(1, 100) < (100 * train_r) for i in range(self.num)]
        # self.train_mask = pd.core.frame.DataFrame([random.randint(1, 100) for i in range(self.num)]) < (100 * train_r)
        self.test_mask = [not i for i in self.train_mask]

        # print(self.train_mask)
        # print(self.test_mask)

    def preprocess(self):
        train_data = self.data.loc[self.train_mask, :]
        train_features = train_data.iloc[:, :-1]
        self.train_min = train_features.min(axis = 0)
        self.train_max = train_features.max(axis = 0)
        self.train_features = (train_features - self.train_min) / (self.train_max - self.train_min)
        self.train_labels = train_data['label']

        test_data = self.data.loc[self.test_mask, :]
        test_features = test_data.iloc[:, :-1]
        self.test_features = (test_features - self.train_min) / (self.train_max - self.train_min)
        self.test_labels = test_data['label']

        # print(self.train_labels)
    def euclidean_dist(self, sample_1, sample_2):
        sample_delta = sample_1 - sample_2
        dist = 0
        for ii in range(len(sample_delta)):
            dist += sample_delta[ii] ** 2
        dist = math.sqrt(dist)
        return dist

    def find_top_k_label(self, sample_1): # return the major vote
        top_k_hq = []
        # print(self.train_features.shape)
        for ii in range(self.train_features.shape[0]):
            cur_sample = self.train_features.iloc[ii, :]
            dist = self.euclidean_dist(sample_1, cur_sample)
            if len(top_k_hq) < self.k:
                top_k_hq.append((-dist, ii))
                if len(top_k_hq) == self.k:
                    heapq.heapify(top_k_hq)
            else:
                heapq.heappushpop(top_k_hq, (-dist, ii))

        votes = {}
        while top_k_hq:
            cur = heapq.heappop(top_k_hq)
            # print(cur[1])
            # print(self.test_labels.shape)
            cur_vote = self.train_labels.iloc[cur[1]]
            if cur_vote in votes:
                votes[cur_vote] += 1
            else:
                votes[cur_vote] = 1

        max_vote = []
        for k in votes:
            if max_vote:
                if votes[k] > max_vote[1]:
                    max_vote = [k, votes[k]]
            else:
                max_vote = [k, votes[k]]
        return max_vote[0]

    def validate(self):
        self.correct_num = 0
        for ii in range(self.test_features.shape[0]):
            cur_feature = self.test_features.iloc[ii, :]
            cur_label = self.test_labels.iloc[ii]
            pred_label = self.find_top_k_label(cur_feature)
            # print(f'cur: {cur_label}, pred: {pred_label}')
            if cur_label == pred_label:
                self.correct_num += 1
        
        self.acc = self.correct_num / self.test_features.shape[0]
        
        print(f'Accuracy is {self.acc} \n')



# #data loading option 1
# with open('iris.data', 'rb') as csvfile:
#     lines = csv.reader(csvfile)
#     for row in lines:
#         print ', '.join(row)
#or
#data loading option 2
def loadData() :
    # 0 setosa	1 versicolor 2 virginica
    data = pd.read_csv('iris.csv')
    data.columns = ['seplen', 'sepwid', 'petlen', 'petwid', 'label']
    return data        


if __name__ == "__main__":
    data = loadData()
    case_1 = kNN(data=data, k = 5)
    case_1.split_dataset()
    case_1.preprocess()
    case_1.validate()
      
# print('Accuracy: %.3f%%' % (correct / len(knn.valData)))

