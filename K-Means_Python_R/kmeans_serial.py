import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import timeit
import seaborn as sns


def elbow(vals, timer_start):
    plt.figure('Elbow Graph showing the optimal amount of clusters k')
    plt.plot(range(1, 10), vals, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    print(f'Time up to here is: {timeit.default_timer() - timer_start}')
    plt.show()


def centroids(kmeanModel, labels):
    cluster = plt.figure(1)
    plt.scatter(list(kmeanModel.cluster_centers_[:, 0]), list(kmeanModel.cluster_centers_[:, 1]), cmap='rainbow')
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.title('Price and Speed of the cluster centroids')


def heatmap(df, timer_start):
    avg = df.groupby(['Cluster']).mean()
    Price_max = round(avg['price'].max(), 2)
    print(f'Cluster with highest Price avg has price = {Price_max} ')

    # Plotting the heatmap
    heat = plt.figure('Heatmap for the cluster centroids')
    avg = avg.drop(['id', 'cd', 'multi', 'premium'], axis=1)
    sns.heatmap(avg, annot=True, cmap="YlGnBu")
    print(f'Time of second part: {timeit.default_timer() - timer_start}')
    plt.show()


if __name__ == "__main__":

    # load csv
    start = timeit.default_timer()
    df = pd.read_csv('computers.csv', encoding="ISO-8859-1", sep=";")
    df = df.rename(columns={df.columns[0]: "id"})

    # make values numeric
    df[['cd', 'multi', 'premium']] = df[['cd', 'multi', 'premium']].replace({'yes': 1, 'no': 0})

    # to numpy array
    data = df.values[:, 1:]
    labels = df.columns[1:]

    # plot the elbow graph
    elbow([KMeans(n_clusters=k).fit(data).inertia_ for k in range(1, 10)], start)

    # fit the data
    n_clusters = int(input('How many clusters?: '))
    restart_timer = timeit.default_timer()
    kmeanModel = KMeans(n_clusters)
    kmeanModel.fit(data)
    identified_clusters = kmeanModel.fit_predict(data)
    df['Cluster'] = identified_clusters

    # Plotting the centroids of first two dimensions
    centroids(kmeanModel, labels)

    # Getting the average of each cluster
    heatmap(df, restart_timer)
