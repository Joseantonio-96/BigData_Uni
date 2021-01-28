import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import timeit
import seaborn as sns
from threading import Thread
from kmeans_serial import elbow, centroids, heatmap

# load csv
start = timeit.default_timer()
df = pd.read_csv('computers.csv', encoding="ISO-8859-1", sep=";")
df = df.rename(columns={df.columns[0]: "id"})

# number of threads = number of clusters
n_threads = 10

def loop(j, func):
    for f in func:
        for i in j:
            f(i)


def thread_cluster(data_, threads):
    cluster_inertia = {}
    jobs = [Thread(target=inertia, args=(data_, i, cluster_inertia)) for i in range(1, threads)]
    loop(jobs, [Thread.start, Thread.join])
    return cluster_inertia


def inertia(data_, n, cluster_inertia):
    cluster_inertia[n] = KMeans(n_clusters=n).fit(data_).inertia_


# make values numeric
df[['cd', 'multi', 'premium']] = df[['cd', 'multi', 'premium']].replace({'yes': 1, 'no': 0})

# to numpy array
data = df.values[:, 1:]
labels = df.columns[1:]
inertia_per_cluster = thread_cluster(data, n_threads)

# plot the elbow graph
elbow([inertia_per_cluster[i] for i in range(1,n_threads)], start)

# fit the data
n_clusters = int(input('How many clusters?: '))
start = timeit.default_timer()
kmeanModel = KMeans(n_clusters).fit(data)
identified_clusters = kmeanModel.predict(data)
df['Cluster'] = identified_clusters

# Plotting the centroids of first two dimensions
centroids(kmeanModel, labels)

# Plotting the heatmap
heatmap(df, start)
