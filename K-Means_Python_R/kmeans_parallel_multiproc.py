import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import timeit
import seaborn as sns
from multiprocessing import Pool, cpu_count
from sklearn.preprocessing import StandardScaler
from kmeans_serial import elbow, centroids, heatmap

# using pool.apply_async
results = []


def parallelize_inertia(func, data_, n_cores=cpu_count()):
    pool = Pool(n_cores)
    for i in range(1, 10):
        pool.apply_async(func, args=(data_, i), callback=collect_result)
    pool.close()
    pool.join()
    return results


def collect_result(result):
    global results
    results.append(result)


def inertia(data_, n):
    return [KMeans(n_clusters=n).fit(data_).inertia_]


# load csv
start = timeit.default_timer()
df = pd.read_csv('computers.csv', encoding="ISO-8859-1", sep=";")
df = df.rename(columns={df.columns[0]: "id"})
# make values numeric
df[['cd', 'multi', 'premium']] = df[['cd', 'multi', 'premium']].replace({'yes': 1, 'no': 0})

# to numpy array
data = df.values[:, 1:]
labels = df.columns[1:]
inertia_values = parallelize_inertia(inertia, data)

# plot the elbow graph
elbow(inertia_values, start)

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
