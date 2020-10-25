import numpy as np
from matplotlib import pyplot as plt

# Python Numpy, ROW MAJOR

class KMeans:
    # initialize and fit
    def __init__(self, data):
        self.data = data
        self.num = self.data.shape[0]


    # Step 1. initialize the k centroids
    def initialize(self, k = 5):
        self.k = k
        centroid_mask = np.random.choice(self.num, size = self.k, replace = False)
        self.centroids = self.data[centroid_mask, :]
       
    # Step 2. calcualte the dist to each centroids
    def dist_calculate_cent_update(self):
        # calculate dist and assign closest centroid
        self.assign_mask = np.zeros(self.num, dtype = 'int')
        for ii in range(self.num):
            self.assign_mask[ii] = np.argmin(np.sum(np.square(self.centroids - self.data[ii, :]), axis = 1))

        # update new centroids
        self.distortion = 0
        for ii in range(self.k):
            self.centroids[ii] = np.mean(self.data[self.assign_mask == ii], axis = 0)
            self.distortion += np.sum(np.sum(np.abs(self.data[self.assign_mask == i] - self.centroids[ii])))


    # Step 3. assign samples to the closest centroids
    # Step 4. update the centroids with the means of the 
    # repeat to step 2, 3 and 4.

    def fit(self, max_iter = 10):
        counter = 0
        while counter < max_iter:
            self.dist_calculate_cent_update()
            self.kmeans_plot()
            counter += 1

    def kmeans_plot(self):
        fig, ax = plt.subplots()
        pts_sc = ax.scatter(self.data[:, 0], self.data[:, 1], c = self.assign_mask, cmap = 'ocean')
        cent_sc = ax.scatter(self.centroids[:, 0], self.centroids[:, 1], marker = 'x', s = 42, color = 'r')
        plt.show()


    # def elbow(self, max_k = 10):
    #     self.k_list = [None] * max_k
    #     for ii in range(max_k):
    #         self.initialize(k  = ii)
    #         self.fit(max_iter = 20)
    #         self.k_list[ii] = self.distortion


    # def elbow_plot(self):
    #     fig, ax = plt.subplot()
    #     x = [i for i in range(len(self.distortion))]
    #     ax.plots(x, k_list)




class DataGeneration:
    def __init__(self):
        self.data = self.ambers_random_data()

    def ambers_random_data(self):
        np.random.seed(1)
        x = 2
        data1 = np.random.normal(size=(100, 2)) + [ x, x]
        data2 = np.random.normal(size=(100, 2)) + [ x,-x]
        data3 = np.random.normal(size=(100, 2)) + [-x,-x]
        data4 = np.random.normal(size=(100, 2)) + [-x, x]
        data5 = np.random.normal(size=(100, 2)) + [-x,-x]
        data6 = np.random.normal(size=(100, 2)) + [-x, x]
        data  = np.concatenate((data1, data2, data3, data4, data5, data6))
        np.random.shuffle(data)
        self.data = data
        return data

#plots
    #def elbow plot:
        #ax.set_xlabel("Number of Clusters")
        #ax.set_ylabel("Distortion")
        #print("Showing the elbow plot. Close the plot window to continue.")
        #plt.show()
    #def kmeans cluster plot: 
        #get num of clusters
        #ax.scatter(
        #ax.legend()
        #plt.show()
if __name__ == "__main__":
    generator = DataGeneration()
    k_means = KMeans(generator.data)
    k_means.elbow()
    k_means.elbow_plot()
    k = input("Choose number of clusters: ")
    k_means.initialize(int(k))
    k_means.fit()
    k_means.kmeans_plot()
