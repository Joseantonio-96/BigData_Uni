import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import timeit
import seaborn as sns
from multiprocessing import Pool, cpu_count
from kmeans_serial import elbow, centroids, heatmap

# using pool.apply_async
results = []


def parallelize_fit(func, data_, n_cores=cpu_count()):
    pool = Pool(n_cores)
    for i in range(1, 10):
        pool.apply_async(func, args=(data_, i), callback=collect_result)
    pool.close()
    pool.join()
    return results


def parallelize_inertia(data_, n_cores=cpu_count()):
    pool = Pool(n_cores)
    res = [pool.apply(inertia, args=(i, )) for i in data_]
    pool.close()
    pool.join()
    return res


def collect_result(r):
    global results
    results.append(r)


def fitdata(data_, n):
    return KMeans(n_clusters=n).fit(data_)


def inertia(data_):
    return data_.inertia_

# load csv
start = timeit.default_timer()
df = pd.read_csv('computers.csv', encoding="ISO-8859-1", sep=";")
df = df.rename(columns={df.columns[0]: "id"})
# make values numeric
df[['cd', 'multi', 'premium']] = df[['cd', 'multi', 'premium']].replace({'yes': 1, 'no': 0})

# to numpy array
data = df.values[:, 1:]
labels = df.columns[1:]
fitd = parallelize_fit(fitdata, data)
inertia_values = parallelize_inertia(fitd)

# Elbow Plot
elbow(inertia_values, start)
# ### Parallelization up to here ####

# fit the data
n_clusters = int(input('How many clusters?: '))
start = timeit.default_timer()
kmeanModel = fitd[n_clusters-1]
identified_clusters = kmeanModel.fit_predict(data)
df['Cluster'] = identified_clusters


# Plotting the centroids of first two dimensions
centroids(kmeanModel, labels)

# Getting the average of each cluster
heatmap(df,start)
